import math
from datetime import timedelta

import pyotp
from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import AuditLog, Loan, LoanReceipt, ResourceItem, Sanction, Student, User
from .selectors import student_can_borrow
from .validations import validate_term


class ItemNotAvailable(APIException):
    """Returns 409 Conflict when the item is already lent or can't be lent."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'El ejemplar no está disponible.'
    default_code = 'item_not_available'


# ---------- audit log ----------

def record_audit_event(user: User, action: str, entity_name: str, entity_id: int,
                       ip_address: str = None) -> AuditLog:
    """RNF-05: saves who did what and from which IP."""
    return AuditLog.objects.create(
        user=user,
        action=action,
        entity_name=entity_name,
        entity_id=entity_id,
        ip_address=ip_address,
    )


# ---------- users ----------

def create_staff_user(data: dict, created_by: User = None, ip_address: str = None) -> User:
    """RF-02 / RF-03: creates an admin or operator. Password is hashed by create_user()."""
    password = data.pop('password', None)
    if data.get('is_temporary') and not data.get('valid_until'):
        raise serializers.ValidationError(
            {'valid_until': 'Una cuenta temporal necesita fecha de caducidad'}
        )
    user = User.objects.create_user(password=password, **data)
    generate_mfa_secret(user)
    if created_by:
        record_audit_event(created_by, 'USER_CREATED', 'User', user.id, ip_address)
    return user


def deactivate_user(user: User, done_by: User, ip_address: str = None) -> User:
    """RF-02: soft delete, we never delete users from the database."""
    user.is_active = False
    user.save(update_fields=['is_active'])
    record_audit_event(done_by, 'USER_DEACTIVATED', 'User', user.id, ip_address)
    return user


def expire_temporary_accounts() -> int:
    """RN-02: turns off temporary accounts whose valid_until already passed."""
    now = timezone.now()
    return User.objects.filter(
        is_temporary=True, is_active=True, valid_until__lt=now
    ).update(is_active=False)


# ---------- MFA (RF-01) ----------

MFA_CHALLENGE_SALT = 'apiGit.mfa-challenge'
MFA_CHALLENGE_MAX_AGE = 300  # 5 minutos para completar el segundo factor


def generate_mfa_secret(user: User) -> str:
    """RF-01: creates the TOTP secret used as the staff's second login factor."""
    secret = pyotp.random_base32()
    user.mfa_secret = secret
    user.save(update_fields=['mfa_secret'])
    return secret


def build_mfa_provisioning_uri(user: User) -> str:
    """URI (QR) to enroll the secret in an authenticator app, shown only once."""
    return pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(
        name=user.email, issuer_name='Biblioteca INACAP'
    )


def create_mfa_challenge(user: User) -> str:
    """Short-lived token issued after step 1 (password); it's not a session yet."""
    return signing.dumps({'user_id': user.id}, salt=MFA_CHALLENGE_SALT)


def resolve_mfa_challenge(challenge: str) -> User:
    """Decodes the challenge from /auth/login/ and returns the pending user."""
    try:
        data = signing.loads(
            challenge, salt=MFA_CHALLENGE_SALT, max_age=MFA_CHALLENGE_MAX_AGE
        )
    except signing.BadSignature:
        raise serializers.ValidationError(
            {'mfa_challenge': 'El challenge es inválido o expiró, inicia sesión de nuevo'}
        )
    try:
        return User.objects.get(pk=data['user_id'], is_active=True)
    except User.DoesNotExist:
        raise serializers.ValidationError(
            {'mfa_challenge': 'El challenge es inválido o expiró, inicia sesión de nuevo'}
        )


def verify_mfa_code(user: User, code: str) -> bool:
    """RF-01: checks the 6-digit TOTP code, tolerating one 30s window of drift."""
    if not user.mfa_secret:
        return False
    return pyotp.TOTP(user.mfa_secret).verify(code, valid_window=1)


# ---------- students ----------

def deactivate_student(student: Student, done_by: User, ip_address: str = None) -> Student:
    student.is_active = False
    student.save(update_fields=['is_active'])
    record_audit_event(done_by, 'STUDENT_DEACTIVATED', 'Student', student.id, ip_address)
    return student


# ---------- loans ----------

def calculate_due_at(start, term_value: int, term_unit: str):
    if term_unit == 'HOURS':
        return start + timedelta(hours=term_value)
    return start + timedelta(days=term_value)


@transaction.atomic
def create_loan(resource_item: ResourceItem, student: Student, operator: User,
                term_value: int, ip_address: str = None) -> Loan:
    """RF-06: registers a loan, marks the item as ON_LOAN and sends the receipt."""
    # lock the row so two operators can't lend the same item at the same time
    item = ResourceItem.objects.select_for_update().select_related(
        'resource_title__category'
    ).get(pk=resource_item.pk)

    if item.status != ResourceItem.Status.AVAILABLE:
        raise ItemNotAvailable()

    can_borrow, reason = student_can_borrow(student)
    if not can_borrow:
        raise serializers.ValidationError({'student': reason})

    # the term unit comes from the category (hours for equipment, days for books)
    term_unit = item.resource_title.category.term_unit
    validate_term(term_value, term_unit)

    now = timezone.now()
    loan = Loan.objects.create(
        resource_item=item,
        student=student,
        checked_out_by=operator,
        term_value=term_value,
        term_unit=term_unit,
        due_at=calculate_due_at(now, term_value, term_unit),
    )

    item.status = ResourceItem.Status.ON_LOAN
    item.save(update_fields=['status'])

    record_audit_event(operator, 'LOAN_CREATED', 'Loan', loan.id, ip_address)

    # the email is sent only if the transaction is saved correctly
    transaction.on_commit(lambda: send_loan_receipt(loan))
    return loan


def send_loan_receipt(loan: Loan) -> LoanReceipt:
    """RF-07: sends the receipt to the student's email and saves the timestamp."""
    item_title = loan.resource_item.resource_title.title
    message = (
        f'Hola {loan.student.first_name},\n\n'
        f'Registramos tu préstamo de: {item_title} ({loan.resource_item.barcode}).\n'
        f'Inicio: {timezone.localtime(loan.started_at):%d-%m-%Y %H:%M}\n'
        f'Debes devolverlo antes de: {timezone.localtime(loan.due_at):%d-%m-%Y %H:%M}\n\n'
        f'Biblioteca INACAP'
    )
    try:
        send_mail(
            subject='Comprobante de préstamo',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[loan.student.institutional_email],
        )
        delivery_status = 'SENT'
    except Exception:
        delivery_status = 'FAILED'

    # if it was already sent before (resend), we update the same receipt
    receipt, _created = LoanReceipt.objects.update_or_create(
        loan=loan,
        defaults={
            'recipient_email': loan.student.institutional_email,
            'delivery_status': delivery_status,
            'sent_at': timezone.now(),
        },
    )
    return receipt


@transaction.atomic
def return_loan(loan: Loan, operator: User, ip_address: str = None) -> Loan:
    """RF-08: registers the return. If it is late, a sanction is created (RF-09)."""
    loan = Loan.objects.select_for_update().get(pk=loan.pk)

    if loan.status == Loan.Status.RETURNED:
        raise serializers.ValidationError({'detail': 'Este préstamo ya fue devuelto.'})

    now = timezone.now()
    loan.returned_at = now
    loan.checked_in_by = operator
    loan.status = Loan.Status.RETURNED
    loan.save(update_fields=['returned_at', 'checked_in_by', 'status'])

    item = loan.resource_item
    item.status = ResourceItem.Status.AVAILABLE
    item.save(update_fields=['status'])

    record_audit_event(operator, 'ITEM_RETURNED', 'Loan', loan.id, ip_address)

    if now > loan.due_at:
        apply_late_return_sanction(loan)

    return loan


# rule: 1 day of block for each hour (or part of an hour) of delay
SANCTION_RULE = '1_DAY_PER_HOUR_LATE'


def apply_late_return_sanction(loan: Loan) -> Sanction:
    """RF-09: calculates the end of the block depending on the minutes late."""
    minutes_late = int((loan.returned_at - loan.due_at).total_seconds() // 60)
    minutes_late = max(minutes_late, 1)
    days_blocked = math.ceil(minutes_late / 60)

    return Sanction.objects.create(
        student=loan.student,
        loan=loan,
        minutes_late=minutes_late,
        starts_at=loan.returned_at,
        ends_at=loan.returned_at + timedelta(days=days_blocked),
        rule_applied=SANCTION_RULE,
    )


def mark_overdue_loans() -> int:
    """Changes ACTIVE loans that passed their due date to OVERDUE."""
    now = timezone.now()
    return Loan.objects.filter(status=Loan.Status.ACTIVE, due_at__lt=now).update(
        status=Loan.Status.OVERDUE
    )


def finish_expired_sanctions() -> int:
    """Sanctions whose ends_at already passed are no longer active."""
    now = timezone.now()
    return Sanction.objects.filter(is_active=True, ends_at__lte=now).update(is_active=False)
