from django.contrib import admin
from .models import Student, Employee, Course, Class, Enrollment, Session, Attendance
from .models import Exam, ExamSection, StudentGrade, OralGrade, PlacementTestRequest
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
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['class_group', 'date', 'start_time', 'end_time', 'is_cancelled']
    list_filter = ['is_cancelled', 'date', 'class_group']
    raw_id_fields = ['class_group']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status']
    list_filter = ['status', 'session__date']
    raw_id_fields = ['student', 'session']
    
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['class_group', 'total_score', 'status']

@admin.register(ExamSection)
class ExamSectionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'name', 'max_score']

@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_section', 'score']

@admin.register(OralGrade)
class OralGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'score']

@admin.register(PlacementTestRequest)
class PlacementTestRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'test_type', 'status', 'approved_level']