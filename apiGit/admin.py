from django.contrib import admin
from .models import Sanction, Student, ResourceTitle, ResourceItem, LoanReceipt, Category, Loan, AuditLog, User

# Register your models here.

admin.site.register([Sanction, Student, ResourceItem, ResourceTitle, Loan, LoanReceipt, Category, AuditLog, User])