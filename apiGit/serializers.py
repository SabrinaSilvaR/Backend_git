from rest_framework import serializers
from .models import User, Student, Category, ResourceTitle, ResourceItem, Loan, Sanction, AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         password=validated_data['password']
    #     )
    #     return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =  '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =  '__all__'

class ResourceTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceTitle
        fields = '__all__'

class ResourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
class SanctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanction
        fields = '__all__'  # Include all fields in the Sanction model

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'  # Include all fields in the AuditLog model