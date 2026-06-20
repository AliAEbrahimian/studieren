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
    path('exams/dashboard/', views.exam_dashboard, name='exam_dashboard'),
    path('myProfile/', lambda request: redirect('dashboard')),
    
    path('student/scores/', views.student_scores, name='student_scores'),
    path('student/finance/', views.student_finance, name='student_finance'),
    path('class/<int:class_id>/students/', views.class_students, name='class_students'),
    path('placement/request/', views.request_placement_test, name='request_placement_test'),
    
    path('class/<int:class_id>/sessions/generate/', views.generate_class_sessions, name='generate_sessions'),
    path('class/<int:class_id>/attendance/', views.attendance_sheet, name='attendance_sheet'),
    path('class/<int:class_id>/attendance/export/', views.export_attendance_excel, name='export_attendance_excel'),
    
    path('teacher/classes/', views.teacher_classes, name='teacher_classes'),
    path('teacher/schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    
    path('staff/login/', views.staff_login, name='staff_login'),
    
    path('exam/<int:exam_id>/written/', views.enter_written_grades, name='enter_written_grades'),
    path('exam/<int:exam_id>/oral/', views.enter_oral_grades, name='enter_oral_grades'),
    path('exam/<int:exam_id>/finalize/', views.finalize_exam, name='finalize_exam'),
    path('exams/finalized/', views.finalized_exam_list, name='finalized_exam_list'),
    path('exams/', views.exam_list, name='exam_list'),
    path('class/<int:class_id>/create-exam/', views.create_exam, name='create_exam'),

    

    
    path('error-test/', lambda request: render(request, 'base/error.html', {'message': 'Test message'})),
    
    path('', lambda request: redirect('dashboard'), name="home"),
]