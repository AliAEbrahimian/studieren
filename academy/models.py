from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
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
    
    def __str__(self):
        code = self.class_code or "?"
        teacher_name = self.teacher.user.get_full_name() if self.teacher else 'No Teacher'
        return f"[{code}] {self.title} - {teacher_name}"
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        
        
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