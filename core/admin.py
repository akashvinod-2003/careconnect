from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceRequest

# 1. Configure User Manager
class CustomUserAdmin(UserAdmin):
    model = User
    # Show these fields in the list
    list_display = ['username', 'email', 'role', 'title', 'is_staff']
    # Add filters on the right side
    list_filter = ['role', 'is_staff', 'is_active']
    
    # Add 'role' to the edit page
    fieldsets = list(UserAdmin.fieldsets) + [
        ('Role Info', {'fields': ('role', 'phone', 'title')}),
    ]

    # Add 'role' to the creation page (This fixes the issue)
    add_fieldsets = list(UserAdmin.add_fieldsets) + [
        ('Role Info', {'fields': ('role', 'phone', 'title')}),
    ]

# 2. Configure Request Manager
class RequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'service_type', 'status', 'assigned_staff', 'created_at']
    list_filter = ['status', 'service_type']
    search_fields = ['patient_name', 'location']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceRequest, RequestAdmin)