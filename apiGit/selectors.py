from django.db.models import Count, Q
from django.utils import timezone

from .models import Loan, ResourceItem, ResourceTitle, Sanction, Student


def student_can_borrow(student: Student) -> tuple[bool, str]:
    """RN-03: a student can't borrow if they have an active sanction or an overdue loan."""
    now = timezone.now()

    if not student.is_active:
        return False, 'Alumno inactivo'

    has_sanction = Sanction.objects.filter(
        student=student, is_active=True, ends_at__gt=now
    ).exists()
    if has_sanction:
        return False, 'Sanción vigente'

    has_overdue = Loan.objects.filter(
        student=student, status__in=['ACTIVE', 'OVERDUE'], due_at__lt=now
    ).exists()
    if has_overdue:
        return False, 'Préstamo vencido sin devolver'

    return True, ''


def list_loans(status: str = None, operator_id: str = None, student_id: str = None):
    loans = Loan.objects.select_related(
        'resource_item__resource_title', 'student', 'checked_out_by', 'checked_in_by'
    ).order_by('-started_at')
    if status:
        loans = loans.filter(status=status)
    if operator_id:
        loans = loans.filter(checked_out_by_id=operator_id)
    if student_id:
        loans = loans.filter(student_id=student_id)
    return loans


def list_overdue_loans():
    now = timezone.now()
    return list_loans().filter(status__in=['ACTIVE', 'OVERDUE'], due_at__lt=now)


def list_student_loan_history(student: Student):
    return list_loans(student_id=student.id)


def get_item_by_barcode(barcode: str):
    return ResourceItem.objects.select_related('resource_title__category').get(barcode=barcode)


def list_catalog_with_availability(category_id: str = None, search: str = None):
    """Counts total and available items per title (counter view, RF-05)."""
    titles = ResourceTitle.objects.filter(is_active=True).select_related('category')
    if category_id:
        titles = titles.filter(category_id=category_id)
    if search:
        titles = titles.filter(
            Q(title__icontains=search) | Q(author_or_brand__icontains=search)
        )
    titles = titles.annotate(
        total_items=Count('items', filter=~Q(items__status='RETIRED')),
        available_items=Count('items', filter=Q(items__status='AVAILABLE')),
    )
    return titles.order_by('title')


def inventory_report():
    """How many items there are per category and status."""
    return (
        ResourceItem.objects.values('resource_title__category__name', 'status')
        .annotate(total=Count('id'))
        .order_by('resource_title__category__name', 'status')
    )


def shift_summary(operator, since):
    loans_given = Loan.objects.filter(checked_out_by=operator, started_at__gte=since).count()
    loans_received = Loan.objects.filter(
        checked_in_by=operator, returned_at__gte=since
    ).count()
    return {
        'operator': operator.username,
        'since': since,
        'loans_given': loans_given,
        'loans_received': loans_received,
    }
