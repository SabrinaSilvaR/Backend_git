from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Student, Category, ResourceTitle, ResourceItem, Loan, Sanction, AuditLog
from .serializers import UserSerializer, StudentSerializer, CategorySerializer, ResourceTitleSerializer, ResourceItemSerializer, LoanSerializer, SanctionSerializer, AuditLogSerializer 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ResourceTitleViewSet(viewsets.ModelViewSet):
    queryset = ResourceTitle.objects.all()
    serializer_class = ResourceTitleSerializer

class ResourceItemViewSet(viewsets.ModelViewSet):
    queryset = ResourceItem.objects.all()
    serializer_class = ResourceItemSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class SanctionViewSet(viewsets.ModelViewSet):
    queryset = Sanction.objects.all()
    serializer_class = SanctionSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer