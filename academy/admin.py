from django.contrib import admin
from .models import Student, Employee, Course, Class, Enrollment
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrollment_date', 'current_level']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'department', 'supervisor']
    list_filter = ['position', 'department']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user', 'supervisor']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'level']
    
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_code', 'title', 'course', 'teacher', 'class_type', 'start_date', 'capacity']
    list_filter = ['class_type', 'course__language', 'start_date']
    raw_id_fields = ['teacher']
    search_fields = ['class_code', 'title', 'course__title']
    readonly_fields = ['class_code']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'enrolled_class', 'payment_status', 'registration_date']
    list_filter = ['payment_status', 'enrolled_class']
    raw_id_fields = ['student', 'enrolled_class']