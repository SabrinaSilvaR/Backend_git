from rest_framework import serializers
from .models import User, Student, Category, ResourceTitle, ResourceItem, Loan, Sanction, AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_temporary',
            'valid_from',
            'valid_until',
            'is_active',
            'password',
            'mfa_secret',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'mfa_secret': {'write_only': True, 'required': False},
        }

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop('password', None)
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'rut',
            'institutional_email',
            'first_name',
            'last_name',
            'is_active',
            'created_at',
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'term_unit', 'is_active']

class ResourceTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceTitle
        fields = [
            'id',
            'category',
            'title',
            'author_or_brand',
            'reference_code',
            'is_active',
        ]

class ResourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = [
            'id',
            'resource_title',
            'barcode',
            'status',
            'location',
            'acquired_at',
        ]

class LoanSerializer(serializers.ModelSerializer):
    resource_item_title = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'id',
            'resource_item',
            'resource_item_title',
            'student',
            'student_name',
            'checked_out_by',
            'checked_in_by',
            'started_at',
            'term_value',
            'term_unit',
            'due_at',
            'returned_at',
            'status',
        ]

    def get_resource_item_title(self, obj: Loan) -> str:
        return obj.resource_item.resource_title.title
    def get_student_name(self, obj:Loan)->str:
        return f"{obj.student.first_name} {obj.student.last_name}"

    def validate(self, attrs):
        if self.instance is None and self.initial_data.get('checked_in_by'):
            raise serializers.ValidationError(
                {'checked_in_by': 'No se puede enviar este campo al crear.'}
            )

        resource_item = attrs.get('resource_item')
        if resource_item:
            active_loans = Loan.objects.filter(resource_item=resource_item, status='ACTIVE')
            if self.instance is not None:
                active_loans = active_loans.exclude(pk=self.instance.pk)
            if active_loans.exists():
                raise serializers.ValidationError(
                    {'resource_item': 'Este ejemplar ya tiene un préstamo activo.'}
                )

        return attrs


class SanctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanction
        fields = [
            'id',
            'student',
            'loan',
            'minutes_late',
            'starts_at',
            'ends_at',
            'rule_applied',
            'is_active',
        ]

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user',
            'action',
            'entity_name',
            'entity_id',
            'ip_address',
            'created_at',
        ]