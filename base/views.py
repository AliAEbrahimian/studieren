# Django core imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings

# Python standard library
from datetime import date

# Local apps - models
from .models import UserAccount
from academy.models import Student, Employee, Course, Class, Enrollment

# Local apps - forms
from .forms import RegisterForm, UserUpdateForm

from .models import  UserAccount
from django.contrib import messages


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
                login(request, user)
                return redirect('dashboard')
        else:
                messages.error(request, 'Invalid email or password.')
        
    context = {'page' : 'login'}
    return render(request, 'base/login.html', context)

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
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')
            
            send_mail(
                subject='Activate your account',
                message=f'Hi {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nIf you did not sign up, ignore this message.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
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
            send_mail(
                subject = 'Reset Password',
                message = f"Hello {user.username},\nWe received a request to reset your password."
                + " To create a new one, please click the link below:"
                + f"\n{rese_tlink}\nIf you didnt request this, you can safely ignore this message."
                + "\nThis link will expire in 1 hour."
                + "Best regards,The (Studieren) Team",
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [user.email],
                fail_silently = True,
            )
        except User.DoesNotExist:
            pass
        
        messages.success(request, 'If an account exists with this email, an email containing a recovery link will be sent to you.')
        return redirect('login')
        
    return render(request,'base/resetpassword.html')

def resetPasswordConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except (User.DoesNotExist, ValueError,TypeError):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user, request.POST or None)
        
        if request.method == 'POST':
            
            if form.is_valid():
                form.save()
                messages.success(request,'New password successfully set. Sign in now.')
                request.session.flush()
                return redirect('login')
            else:
                messages.error(request, 'Password does not meet the required conditions.')
                
        context = {'form' : form}
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
        'total_revenue': 0,}
    
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
            taught_classes = employee_profile.taught_classes.all().select_related('course')
            
            
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
def student_scores(request):
    return render(request, 'base/student_scores.html', {'user': request.user})

@login_required(login_url='login')
def student_finance(request):
    return render(request, 'base/student_finance.html', {'user': request.user})



@login_required(login_url='login')
def teacher_classes(request):
    return render(request, 'base/teacher_classes.html', {'user': request.user})

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
    return render(request, 'base/teacher_schedule.html', {'user': request.user})

@login_required(login_url='login')
def teacher_attendance(request):
    return render(request, 'base/teacher_attendance.html', {'user': request.user})

