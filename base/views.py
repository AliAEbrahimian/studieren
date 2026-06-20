# Django core imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings

# Python standard library
from datetime import date
import openpyxl

# Local apps - models
from .models import UserAccount
from academy.models import Student, Employee, Course, Class, Enrollment
from academy.models import Session, Attendance, PlacementTestRequest, Exam, ExamSection, StudentGrade, OralGrade
# Local apps - forms
from .forms import RegisterForm, UserUpdateForm

from .models import  UserAccount


# Create your views here.

#rooms = [
#    {'id' : 1, 'name' : 'Kurs 1'},
#    {'id' : 2, 'name' : 'Kurs 2'},
#    {'id' : 3, 'name' : 'Kurs 3'},
#    {'id' : 4, 'name' : 'Kurs 4'},
#]

User = get_user_model()

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email','').lower()
        password = request.POST.get('password','')
            
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_active:
            
            try:
                emy = user.employee_profile
                messages.error(request, 'This login is for students only. Please use the staff login page.')
                return redirect('login')
            except Employee.DoesNotExist:
                pass
            
            
            login(request, user)
            return redirect('dashboard')
        else:
                messages.error(request, 'Invalid email or password.')
        
    context = {'page' : 'login'}
    return render(request, 'base/login.html', context)

def staff_login(request):
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.is_active:
            
            try:
                employee = user.employee_profile
                
                login(request, user)
                
                if employee.position in [Employee.Position.EXAM_MANAGER, Employee.Position.EXAM_CORRECTOR]:
                    return redirect('exam_dashboard')
                
                return redirect('dashboard')
            except Employee.DoesNotExist:
                
                messages.error(request, 'You do not have staff access. Please use the student login page.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    context = {'page': 'staff_login'}
    return render(request, 'base/staff_login.html', context)

def logoutUser(request):
    logout(request)    
    return redirect('login')

def registerPage(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            
            user.username = user.email.lower()
            
            user.is_active = False
            user.save()
            
            Student.objects.get_or_create(user=user, defaults={'enrollment_date': date.today()})
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')
            
            
            plain_message = (
                f'Hi {user.username},\n\n'
                f'Please click the link below to activate your account:\n'
                f'{activation_link}\n\n'
                f'If you did not sign up, ignore this message.'
            )
            
            
            html_message = f"""
                <p>Hi {user.username},</p>
                <p>Please click the link below to activate your account:</p>
                <p><a href="{activation_link}">Activate My Account</a></p>
                <p>If you did not sign up, ignore this message.</p>
            """
            
            send_mail(
                subject='Activate your account',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Please check your email to activate your account.')
            
            return redirect('login')
            
    return render(request, 'base/register.html', {'form' : form})

def activateAccount(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user =None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('login')

#@login_required(login_url='login')        
#def myProfile(request):
#    context = {'user' : request.user}
#    return render(request,'base/myprofile.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserUpdateForm( instance=user )
            
    context = {'form' : form}
    return render(request, 'base/editprofile.html', context)

def resetPasswordRequest(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            rese_tlink = request.build_absolute_uri(f'/resetpassword/{uid}/{token}/')
            
            
            subject = 'Reset Password'
            message = f"Hello {user.username},\nWe received a request to reset your password. To create a new one, please click the link below:\n\n{rese_tlink}\n\nIf you didnt request this, you can safely ignore this message.\nThis link will expire in 1 hour.\n\nBest regards,\nThe Studieren Team"
            html_message = f"""
                <p>Hello {user.username},</p>
                <p>We received a request to reset your password.</p>
                <p>To create a new one, please click the link below:</p>
                <p><a href="{rese_tlink}">{rese_tlink}</a></p>
                <p>If you didn't request this, you can safely ignore this message.</p>
                <p>This link will expire in 1 hour.</p>
                <br>
                <p>Best regards,</p>
                <p>The Studieren Team</p>
            """
            
            send_mail(
                subject=subject,
                message=message,  
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,  
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass
        
        messages.success(request, 'If an account exists with this email, an email containing a recovery link will be sent to you.')
        return redirect('login')
        
    return render(request,'base/resetpassword.html')

def resetPasswordConfirm(request, uidb64, token):
    # ✅ پاک کردن Session قدیمی برای جلوگیری از تداخل
    request.session.flush()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST or None)
        
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'New password successfully set. Sign in now.')
                return redirect('login')
            else:
                messages.error(request, 'Password does not meet the required conditions.')
                
        context = {'form': form}
        return render(request, 'base/resetpassword_confirm.html', context)
    else:
        messages.error(request, 'The link is not valid or has expired.')
        return redirect('resetpassword')



@login_required(login_url='login')
def dashboard(request):
    user = request.user
    section = request.GET.get('section','overview')
    context = {
        'user': user,
        'total_revenue': 0,
        'today': date.today()
        }
    
    try:
        student_profile = user.student_profile
        context['is_student'] = True
        context['student'] = student_profile
        
        enrollments = Enrollment.objects.filter(
            student=student_profile
            ).select_related('enrolled_class', 'enrolled_class__course', 'enrolled_class__teacher__user')
        
        filter_type = request.GET.get('filter','current')
        today = date.today()
        if filter_type == 'finished':
            enrollments = enrollments.filter(enrolled_class__end_date__lt=today)
        else:
            enrollments = enrollments.filter(enrolled_class__end_date__gte=today)
        
        context['enrollments'] = enrollments
        context['current_filter'] = filter_type
        
        template_name = 'base/dashboard_student.html'
        
    except Student.DoesNotExist:
        context['is_student'] = False
        
    try:
        employee_profile = user.employee_profile
        context['is_employee'] = True
        context['employee'] = employee_profile
        
        if employee_profile.position == Employee.Position.TEACHER:
            #taught_classes = employee_profile.taught_classes.all().select_related('course').order_by('-start_date')
            
            today = date.today()
            taught_classes = employee_profile.taught_classes.filter(end_date__gte=today).select_related('course').order_by('-start_date')
            
            
            today = date.today()
            current_classes = taught_classes.filter(end_date__gte=today)
            finished_classes = taught_classes.filter(end_date__lt=today)
            unique_students = Student.objects.filter(
                enrollments__enrolled_class__teacher=employee_profile
                ).distinct().count()
            total_enrollments = sum(cls.enrollments.count() for cls in taught_classes)
            
            
            
            context['taught_classes'] = taught_classes
            context['current_classes_count'] = current_classes.count()
            context['finished_classes_count'] = finished_classes.count()
            context['total_classes_count'] = taught_classes.count()
            context['unique_students'] = unique_students
            context['total_enrollments'] = total_enrollments
            
            template_name = 'base/dashboard_teacher.html'
        
        elif employee_profile.position in [Employee.Position.EDUCATION_MANAGER, Employee.Position.SENIOR_MANAGER]:
            total_students = Student.objects.count()
            total_teachers = Employee.objects.filter(position = Employee.Position.TEACHER).count()
            total_classes = Class.objects.filter(end_date__gte = date.today()).count()
            context.update({
                'total_students': total_students,
                'total_teachers': total_teachers,
                'total_classes': total_classes,
                'total_revenue': 0
                })
            
            template_name = 'base/dashboard_manager.html'
        
        else:
            template_name = 'base/dashboard_staff.html'
    
    except Employee.DoesNotExist:
        context['is_employee'] = False
        
        if not context.get('is_student'):
            template_name = 'base/dashboard_pending.html'
    
    return render(request, template_name, context)

@login_required(login_url='login')
def exam_dashboard(request):
    user = request.user
    # بررسی دسترسی: فقط کارمندانی که نقش EXAM_MANAGER یا EXAM_CORRECTOR دارند
    try:
        employee = user.employee_profile
        if employee.position not in [Employee.Position.EXAM_MANAGER, Employee.Position.EXAM_CORRECTOR]:
            messages.error(request, 'You do not have permission to access the exam panel.')
            return redirect('dashboard')
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have permission to access the exam panel.')
        return redirect('dashboard')
    
    today = date.today()
    context = {
        'user': user,
        'employee': employee,
        'is_exam_manager': employee.position == Employee.Position.EXAM_MANAGER,
    }
    
    # ----- داده‌های مشترک برای هر دو نقش -----
    # امتحان‌های باز (در حال تصحیح)
    open_exams = Exam.objects.filter(status=Exam.Status.OPEN).select_related('class_group__course').order_by('exam_date')
    context['open_exams'] = open_exams
    
    # ----- داده‌های مخصوص مدیر -----
    if employee.position == Employee.Position.EXAM_MANAGER:
        # کلاس‌هایی که تمام شده‌اند اما هنوز امتحان ندارند
        classes_without_exam = Class.objects.filter(
            end_date__lt=today
        ).exclude(
            id__in=Exam.objects.values_list('class_group_id', flat=True)
        ).select_related('course', 'teacher__user').order_by('-end_date')
        context['classes_without_exam'] = classes_without_exam
        
        # امتحان‌های نهایی شده
        finalized_exams = Exam.objects.filter(status=Exam.Status.FINALIZED).select_related('class_group__course').order_by('-finalized_at')
        context['finalized_exams'] = finalized_exams
        
        template_name = 'base/exam_manager_dashboard.html'
    else:
        template_name = 'base/exam_corrector_dashboard.html'
    
    return render(request, template_name, context)



@login_required(login_url='login')
def student_scores(request):
    return render(request, 'base/student_scores.html', {'user': request.user})

@login_required(login_url='login')
def student_finance(request):
    return render(request, 'base/student_finance.html', {'user': request.user})



@login_required(login_url='login')
def teacher_classes(request):
    user = request.user
    try:
        employee = user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have a teacher profile.')
        return redirect('dashboard')
    
    all_classes = employee.taught_classes.all().select_related('course').order_by('-start_date')
    
    today = date.today()
    
    context = {
        'user': user,
        'employee': employee,
        'all_classes': all_classes,
        'today': today,
    }
    return render(request, 'base/teacher_classes.html', context)

@login_required(login_url='login')
def class_students(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    
    if request.user.employee_profile != cls.teacher:
        return redirect('dashboard')
    
    enrollments = Enrollment.objects.filter(enrolled_class=cls).select_related('student__user')
    context = {
        'cls': cls,
        'enrollments': enrollments,
    }
    return render(request, 'base/class_students.html', context)



@login_required(login_url='login')
def teacher_schedule(request):
    user = request.user
    try:
        employee = user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have a teacher profile.')
        return redirect('dashboard')
    
    today = date.today()
    
    classes = employee.taught_classes.filter(end_date__gte=today).order_by('start_date')
    
    
    from collections import defaultdict
    schedule = defaultdict(list)
    for cls in classes:
        if cls.day_of_week:  
            for day in cls.day_of_week:
                schedule[day].append(cls)
    
    
    for day in schedule:
        schedule[day].sort(key=lambda x: (x.start_time is None, x.start_time))
    
    context = {
        'user': user,
        'employee': employee,
        'schedule': dict(schedule),
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'today': today,
    }
    return render(request, 'base/teacher_schedule.html', context)

@login_required(login_url='login')
def teacher_attendance(request):
    user = request.user
    try:
        employee = user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have a teacher profile.')
        return redirect('dashboard')
    
    today = date.today()
    
    current_classes = employee.taught_classes.filter(
        end_date__gte=today
    ).order_by('start_date')
    
    context = {
        'user': user,
        'current_classes': current_classes,
    }
    return render(request, 'base/teacher_attendance.html', context)

@login_required(login_url='login')
def generate_class_sessions(request, class_id):
    cls = get_object_or_404(Class, id = class_id)
    
    if request.user.employee_profile != cls.teacher and not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    count = cls.generate_sessions()
    messages.success(request, f'{count} new sessions were created successfully.')
    return redirect('attendance_sheet', class_id = class_id)

@login_required(login_url='login')
def attendance_sheet(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    
    if request.user.employee_profile != cls.teacher and not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    sessions = cls.sessions.filter(is_cancelled=False).order_by('date', 'start_time')
    enrollments = Enrollment.objects.filter(
        enrolled_class=cls,
    ).select_related('student__user').order_by('student__user__last_name')
    
    attendance_data = {}
    for enrollment in enrollments:
        student = enrollment.student
        attendance_data[student.pk] = {}
        for session in sessions:
            att, _ = Attendance.objects.get_or_create(
                session=session,
                student=student,
                defaults={'status': Attendance.Status.PRESENT}
            )
            attendance_data[student.pk][session.pk] = att
            
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_'):
                parts = key.split('_')
                student_id = int(parts[1])
                session_id = int(parts[2])
                Attendance.objects.update_or_create(
                    session_id=session_id,
                    student_id=student_id,
                    defaults={'status': value}
                )
                
        messages.success(request, 'Attendance saved successfully.')
        return redirect('attendance_sheet', class_id=class_id)
    context = {
        'cls': cls,
        'sessions': sessions,
        'enrollments': enrollments,
        'attendance_data': attendance_data,
        'today': date.today()
    }
    return render(request, 'base/attendance_sheet.html', context)

@login_required(login_url='login')
def export_attendance_excel(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    
    
    if not request.user.is_staff and request.user.employee_profile != cls.teacher:
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    sessions = cls.sessions.filter(is_cancelled=False).order_by('date', 'start_time')
    enrollments = Enrollment.objects.filter(
        enrolled_class=cls
    ).select_related('student__user').order_by('student__user__last_name')

    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"

    
    ws.cell(row=1, column=1, value="#")
    ws.cell(row=1, column=2, value="Student")
    for col, session in enumerate(sessions, start=3):
        ws.cell(row=1, column=col, value=session.date.strftime("%Y-%m-%d"))

    
    for row, enrollment in enumerate(enrollments, start=2):
        ws.cell(row=row, column=1, value=row-1)
        ws.cell(row=row, column=2, value=enrollment.student.user.get_full_name())
        for col, session in enumerate(sessions, start=3):
            att = Attendance.objects.filter(session=session, student=enrollment.student).first()
            status = att.status if att else 'P'
            ws.cell(row=row, column=col, value=status)

    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=attendance_{cls.class_code}.xlsx'
    wb.save(response)
    return response

@login_required(login_url='login')
def request_placement_test(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Only students can request a placement test.')
        return redirect('dashboard')
    
    open_request = PlacementTestRequest.objects.filter(student=student, status='PENDING').first()
    if open_request:
        messages.warning(request, 'You already have a pending placement test request.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        test_type = request.POST.get('test_type')
        requested_level = request.POST.get('requested_level','')
        
        PlacementTestRequest.objects.create(
            student=student,
            test_type=test_type,
            requested_level=requested_level,
        )
        
        messages.success(request, 'Your placement test request has been submitted.')
        return redirect('dashboard')
    
    context = {
        'user' : request.user,
        'student' : student,
        'test_types' : PlacementTestRequest.TestType.choices,
    }
    
    return render(request, 'base/request_placement_test.html', context)



@login_required(login_url='login')
def enter_written_grades(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # فقط مصحح یا مدیر امتحانات یا مدیر ارشد
    if not request.user.is_staff and request.user.employee_profile.position not in [
        Employee.Position.EXAM_CORRECTOR, Employee.Position.EXAM_MANAGER
    ]:
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    sections = exam.sections.all().order_by('name')
    enrollments = Enrollment.objects.filter(enrolled_class=exam.class_group).select_related('student__user')
    
    if request.method == 'POST':
        for enrollment in enrollments:
            student = enrollment.student
            for section in sections:
                score = request.POST.get(f'score_{student.pk}_{section.pk}')
                if score:
                    StudentGrade.objects.update_or_create(
                        student=student,
                        exam_section=section,
                        defaults={'score': float(score), 'entered_by': request.user.employee_profile}
                    )
        messages.success(request, 'Written grades saved successfully.')
        return redirect('enter_written_grades', exam_id=exam.id)
    
    # ساخت دیکشنری از نمرات موجود
    grades = {}
    for grade in StudentGrade.objects.filter(exam_section__exam=exam).select_related('student', 'exam_section'):
        student_pk = grade.student.pk
        section_pk = grade.exam_section.pk
        if student_pk not in grades:
            grades[student_pk] = {}
        grades[student_pk][section_pk] = grade.score
    
    context = {
        'exam': exam,
        'sections': sections,
        'enrollments': enrollments,
        'grades': grades,
        'is_exam_manager': request.user.employee_profile.position == Employee.Position.EXAM_MANAGER if hasattr(request.user, 'employee_profile') else False,
    }
    return render(request, 'base/enter_written_grades.html', context)

@login_required(login_url='login')
def enter_oral_grades(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    cls = exam.class_group

    # فقط استاد همین کلاس، مدیر امتحانات یا ادمین
    if not request.user.is_staff and (
        not hasattr(request.user, 'employee_profile') or
        (request.user.employee_profile != cls.teacher and
         request.user.employee_profile.position != Employee.Position.EXAM_MANAGER)
    ):
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')

    enrollments = Enrollment.objects.filter(
        enrolled_class=cls
    ).select_related('student__user').order_by('student__user__last_name')

    if request.method == 'POST':
        for enrollment in enrollments:
            student = enrollment.student
            score = request.POST.get(f'oral_score_{student.pk}')
            if score:
                OralGrade.objects.update_or_create(
                    student=student,
                    exam=exam,
                    defaults={
                        'score': float(score),
                        'entered_by': request.user.employee_profile if hasattr(request.user, 'employee_profile') else None
                    }
                )
        messages.success(request, 'Oral grades saved successfully.')
        return redirect('enter_oral_grades', exam_id=exam.id)

    # ساخت دیکشنری از نمرات موجود
    oral_grades = {}
    for grade in OralGrade.objects.filter(exam=exam).select_related('student'):
        oral_grades[grade.student.pk] = grade.score

    context = {
        'exam': exam,
        'enrollments': enrollments,
        'oral_grades': oral_grades,
        'is_exam_manager': request.user.employee_profile.position == Employee.Position.EXAM_MANAGER if hasattr(request.user, 'employee_profile') else False,
    }
    return render(request, 'base/enter_oral_grades.html', context)



@login_required(login_url='login')
def exam_list(request):
    # فقط مدیر امتحانات یا ادمین کل
    if not request.user.is_staff and (
        not hasattr(request.user, 'employee_profile') or
        request.user.employee_profile.position != Employee.Position.EXAM_MANAGER
    ):
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    today = date.today()
    # کلاس‌هایی که تمام شده‌اند ولی امتحان ندارند
    classes_without_exam = Class.objects.filter(
        end_date__lt=today
    ).exclude(
        id__in=Exam.objects.values_list('class_group_id', flat=True)
    ).select_related('course', 'teacher__user').order_by('-end_date')
    
    context = {
        'classes': classes_without_exam,
    }
    return render(request, 'base/exam_list.html', context)

@login_required(login_url='login')
def create_exam(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    # فقط مدیر امتحانات یا ادمین
    if not request.user.is_staff and (
        not hasattr(request.user, 'employee_profile') or
        request.user.employee_profile.position != Employee.Position.EXAM_MANAGER
    ):
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    if hasattr(cls, 'exam'):
        messages.warning(request, 'An exam already exists for this class.')
        return redirect('exam_list')
    
    if request.method == 'POST':
        exam_date = request.POST.get('exam_date')
        total_score = request.POST.get('total_score', 300)
        # ساخت امتحان
        exam = Exam.objects.create(
            class_group=cls,
            exam_date=exam_date,
            total_score=total_score,
        )
        # ساخت بخش‌ها (از پارامترهای POST)
        section_names = request.POST.getlist('section_name[]')
        max_scores = request.POST.getlist('max_score[]')
        for name, max_s in zip(section_names, max_scores):
            if name.strip():
                ExamSection.objects.create(
                    exam=exam,
                    name=name.strip(),
                    max_score=max_s
                )
        messages.success(request, 'Exam created successfully with sections.')
        return redirect('exam_dashboard')
    
    context = {'class': cls}
    return render(request, 'base/create_exam.html', context)

@login_required(login_url='login')
def finalize_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    # فقط مدیر امتحانات یا ادمین کل
    if not request.user.is_staff and (
        not hasattr(request.user, 'employee_profile') or
        request.user.employee_profile.position != Employee.Position.EXAM_MANAGER
    ):
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    if exam.status == Exam.Status.FINALIZED:
        messages.warning(request, 'Exam is already finalized.')
    else:
        exam.status = Exam.Status.FINALIZED
        exam.finalized_by = request.user.employee_profile
        exam.finalized_at = timezone.now()
        exam.save()
        messages.success(request, 'Exam has been finalized. No further changes are allowed.')
    
    return redirect('enter_written_grades', exam_id=exam.id)

 
@login_required(login_url='login')
def finalized_exam_list(request):
    # فقط مدیر امتحانات
    if not request.user.is_staff and (
        not hasattr(request.user, 'employee_profile') or
        request.user.employee_profile.position != Employee.Position.EXAM_MANAGER
    ):
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')
    
    query = request.GET.get('q', '')
    exams = Exam.objects.filter(status=Exam.Status.FINALIZED).select_related('class_group__course').order_by('-finalized_at')
    
    if query:
        exams = exams.filter(
            Q(class_group__title__icontains=query) |
            Q(class_group__class_code__icontains=query) |
            Q(class_group__course__title__icontains=query)
        )
    
    context = {
        'exams': exams,
        'query': query,
    }
    return render(request, 'base/finalized_exam_list.html', context)

