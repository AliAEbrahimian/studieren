from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student_profile'
    )
    
    enrollment_date = models.DateField(auto_now_add=True)
    current_level = models.CharField(max_length=20, blank=True)
    
    def __str__ (self):
        return f"Student: {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        
        
class Employee(models.Model):
    class Position(models.TextChoices):
        TEACHER = 'TEACHER', 'Teacher'
        EDUCATION_MANAGER = 'EDU_MGR', 'Education Manager'
        SENIOR_MANAGER = 'SENIOR_MGR', 'Senior Manager'
        STAFF = 'STAFF', 'Staff'
        
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employee_profile'
    )
    
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.STAFF
    )
    
    department = models.CharField(
        max_length=50,
        blank=True
    )
    
    hire_date = models.DateField(
        null=True,
        blank=True
    )
    
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )
    
    def __str__ (self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}" # type: ignore
    
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        
        
class Course(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    level = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    def __str__ (self):
        return f"{self.title} ({self.level} - {self.language})"
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
     
        
class Class(models.Model):
    class ClassType(models.TextChoices):
        IN_PERSON = 'IN_PERSON', 'In-Person'
        ONLINE = 'ONLINE', 'Online'
        
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='classes'
    )
    
    teacher = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'position': Employee.Position.TEACHER},
        related_name='taught_classes'
    )
    
    title = models.CharField(max_length=100)
    
    class_code = models.PositiveBigIntegerField(
        unique=True,                      # هر کد فقط برای یک کلاس
        blank=True,
        null=True,
        validators=[
            MinValueValidator(100000000), # حداقل ۹ رقم
            MaxValueValidator(999999999)  # حداکثر ۹ رقم
        ],
        verbose_name="Class Code",
        help_text="Unique numeric code in the format YYYYMMNNN (e.g., 140308001)"
    )
    
    capacity = models.PositiveIntegerField(default=10)
    schedule = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    
    class_type = models.CharField(
        max_length=20,
        choices=ClassType.choices,
        default=ClassType.IN_PERSON
    )
    
    meeting_link = models.URLField(
        blank=True,
        help_text="Online meeting link (Google Meet, Zoom, ...)"
    )
    
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Class number or Address of the venue face-to-face classes"
    )
    
    day_of_week = models.JSONField(
        default=list,
        blank=True,
        help_text="Days of the week (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday). Example: [0, 2]"
    )
    
    start_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Start time"
    )
    
    end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="End time"
    )
    
    def _generate_class_code(self):
        if not self.start_date:
            raise ValueError("To generate the class code, the start date cannot be empty.")
        
        year = self.start_date.year
        month = self.start_date.month
        prefix = int(f"{year}{month:02d}")

        last_class = Class.objects.filter(
            class_code__startswith=str(prefix)
        ).order_by('-class_code').first()

        if last_class and last_class.class_code:
            last_code_str = str(last_class.class_code)
            counter = int(last_code_str[6:]) + 1   
            if counter > 999:
                raise ValueError(f"The counter for month {month}/{year} has exceeded 999.")
        else:
            counter = 1
        return int(f"{prefix}{counter:03d}")

    def save(self, *args, **kwargs):
        if not self.class_code and self.start_date:
            self.class_code = self._generate_class_code()
        super().save(*args, **kwargs)
        
    def generate_sessions(self):
        if not self.start_date or not self.end_date or not self.day_of_week:
            return 0
        
        created_count = 0
        current_date = self.start_date
        
        while current_date <= self.end_date:
            if current_date.weekday() in self.day_of_week:
                session_obj, created = Session.objects.get_or_create(
                    class_group=self,
                    date=current_date,
                    start_time=self.start_time,
                    defaults={
                        'end_time': self.end_time,
                        'is_cancelled': False
                    }
                )
                if created:
                    created_count += 1
            current_date += timedelta(days=1)
        return created_count
    
    def __str__(self):
        code = self.class_code or "?"
        teacher_name = self.teacher.user.get_full_name() if self.teacher else 'No Teacher'
        return f"[{code}] {self.title} - {teacher_name}"
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        
class Session(models.Model):
    class_group = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['class_group', 'date', 'start_time']
        ordering = ['date', 'start_time']
        
    def __str__ (self):
        return f"{self.class_group.title} - {self.date}"
    
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'P', 'Present'
        ABSENT = 'A', 'Absent'
        LATE = 'L', 'Late'
        EXCUSED = 'E', 'Excused'
        
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PRESENT
    )
    
    class Meta:
        unique_together = ['session', 'student']
        
    def __str__(self):
        return f"{self.student} - {self.session.date} - {self.get_status_display()}"
        
class Enrollment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        PARTIAL = 'PARTIAL', 'Partial'
        
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
        
    enrolled_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
        
    registration_date = models.DateTimeField(auto_now_add=True)
    
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    class Meta:
        unique_together = ['student', 'enrolled_class']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        
    def __str__ (self):
        return f"{self.student.user.get_full_name()} in {self.enrolled_class.title}"
    
    
class PlacementTestRequest(models.Model):
    class TestType(models.TextChoices):
        IN_PERSON = 'IN_PERSON', 'In-Person Test'
        PREVIOUS_GRADE = 'PREV_GRADE', 'Previous Term Grade'
        
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placement_requests')
    test_type = models.CharField(max_length=20, choices=TestType.choices)
    requested_level = models.CharField(max_length=20, blank=True, help_text="Self-assessed Level (optional)")
    approved_level = models.CharField(max_length=20, blank=True, help_text="Level assigned by manager")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_status = models.CharField(max_length=20, choices=Enrollment.PaymentStatus.choices, default=Enrollment.PaymentStatus.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_test_type_display()} ({self.get_status_display()})"