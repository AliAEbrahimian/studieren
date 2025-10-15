from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room , Topic
from .forms import RoomForm
from django.http import HttpResponse
from .forms import RegisterForm, UserUpdateForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.

#rooms = [
#    {'id' : 1, 'name' : 'Kurs 1'},
#    {'id' : 2, 'name' : 'Kurs 2'},
#    {'id' : 3, 'name' : 'Kurs 3'},
#    {'id' : 4, 'name' : 'Kurs 4'},
#]

User = get_user_model()

def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('myprofile')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Password is incorrect.')
            except User.DoesNotExist:
                messages.error(request, 'User dose not exist.')
        
    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)    
    return redirect('home')

def registerPage(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('myprofile')
        
        else:
            messages.error(request, 'Error regitraition')
            
    return render(request, 'base/login_register.html', {'form' : form})

def myProfile(request):
    return render(request,'base/myprofile.html',{'user' : request.user})

def editProfile(request):
    user = request.user
    form = UserUpdateForm(instance=user)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.user.first_name
            user.last_name = request.user.last_name
            user.birthday = request.user.birthday
            user.phone = request.user.phone
            user.address = request.user.address
            user.postcode = request.user.postcode
            user.save()
            return redirect('myprofile')
        
    context = {'form' : form}
    return render(request, 'base/editprofile.html', context)

def resetPasswordRequest(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'If an account exists with this email, an email containing a recovery link will be sent to you.')
            return redirect('resetpassword')
        
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
        
        messages.success(request, 'An email containing a password change link has been sent.')
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
    


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
                                Q(name__icontains=q)|
                                Q(description__icontains=q))
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms': rooms, 'topics': topics, 'room_count' : room_count}
    return render(request, 'base/home.html' , context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request,'base/room.html', context)


@login_required(login_url='login/')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    
    
    context = { 'form' : form }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login/')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Not worked')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login/')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('Not worked')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html', { 'obj' : room })
