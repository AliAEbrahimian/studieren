from django.contrib import admin
from .models import Invoice
# Register your models here.

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'class_group', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['student__user__email', 'reference_code']
    raw_id_fields = ['student', 'class_group']