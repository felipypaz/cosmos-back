from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","department","role","is_active","hire_date","salary")
    search_fields = ("first_name","last_name","email","department","role","cpf")
    list_filter = ("department","is_active")
