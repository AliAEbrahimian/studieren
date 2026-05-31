from django.urls import path
from . import views
from django.shortcuts import redirect, render

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('activate/<uidb64>/<token>/', views.activateAccount, name='activate'),
    path('editprofile/', views.editProfile, name="editprofile"),
    path('resetpassword/', views.resetPasswordRequest, name="resetpassword"),
    path('resetpassword/<uidb64>/<token>/', views.resetPasswordConfirm, name="resetpasswordconfirm"),
    
    #path('myprofile/', views.myProfile, name="myprofile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('myProfile/', lambda request: redirect('dashboard')),
    
    path('student/scores/', views.student_scores, name='student_scores'),
    path('student/finance/', views.student_finance, name='student_finance'),
    
    path('class/<int:class_id>/students/', views.class_students, name='class_students'),
    path('teacher/classes/', views.teacher_classes, name='teacher_classes'),
    path('teacher/schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),

    
    path('error-test/', lambda request: render(request, 'base/error.html', {'message': 'Test message'})),
    
    path('', views.home , name="home"),
    
    path('room/<int:pk>/', views.room , name="room"),
    
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]