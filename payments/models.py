from django.db import models
from django.conf import settings
from academy.models import Student, Class
# Create your models here.

class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        CANCELED = 'CANCELED', 'Canceled'
        
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    
    class_group = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,       # ← اضافه شود
        blank=True
    )
    
    placement_request = models.ForeignKey(
        'academy.PlacementTestRequest',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True,
        verbose_name="Placement Test Request"
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Calculated tax amount")
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    reference_code = models.CharField(max_length=50, blank=True, unique=True, help_text="Unique tracking code for this invoice.")
    
    def __str__(self):
        return f"Invoice #{self.id} - {self.student.user.get_full_name()} - {self.class_group.title}({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']