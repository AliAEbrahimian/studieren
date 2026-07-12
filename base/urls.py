from django.urls import path
from . import views
from django.shortcuts import redirect, render

urlpatterns = [
    # ============================================================
    # 1. AUTHENTICATION & USER PROFILE
    # ============================================================
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('activate/<uidb64>/<token>/', views.activateAccount, name='activate'),
    path('resetpassword/', views.resetPasswordRequest, name="resetpassword"),
    path('resetpassword/<uidb64>/<token>/', views.resetPasswordConfirm, name="resetpasswordconfirm"),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('editprofile/', views.editProfile, name="editprofile"),

    # ============================================================
    # 2. MAIN DASHBOARD (Role-Based)
    # ============================================================
    path('dashboard/', views.dashboard, name="dashboard"),
    path('myProfile/', lambda request: redirect('dashboard')),

    # ============================================================
    # 3. STUDENT PANEL
    # ============================================================
    path('student/scores/', views.student_scores, name='student_scores'),
    path('student/finance/', views.student_finance, name='student_finance'),
    path('courses/', views.available_courses, name='available_courses'),
    path('class/<int:class_id>/detail/', views.class_detail, name='class_detail'),
    path('class/<int:class_id>/enroll/', views.enroll_class, name='enroll_class'),
    path('class/<int:class_id>/review/', views.enroll_review, name='enroll_review'),
    path('placement/request/', views.request_placement_test, name='request_placement_test'),
    path('placement/status/', views.student_placement_status, name='student_placement_status'),
    

    # ============================================================
    # 4. TEACHER PANEL
    # ============================================================
    path('teacher/classes/', views.teacher_classes, name='teacher_classes'),
    path('teacher/schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('teacher/<int:teacher_id>/schedule/', views.teacher_schedule, name='teacher_schedule_view'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('class/<int:class_id>/students/', views.class_students, name='class_students'),
    path('class/<int:class_id>/sessions/generate/', views.generate_class_sessions, name='generate_sessions'),
    path('class/<int:class_id>/attendance/', views.attendance_sheet, name='attendance_sheet'),
    path('class/<int:class_id>/attendance/export/', views.export_attendance_excel, name='export_attendance_excel'),

    # ============================================================
    # 5. EXAM PANEL (Manager, Corrector & Teacher)
    # ============================================================
    path('exams/dashboard/', views.exam_dashboard, name='exam_dashboard'),
    path('exams/', views.exam_list, name='exam_list'),
    path('class/<int:class_id>/create-exam/', views.create_exam, name='create_exam'),
    path('exam/<int:exam_id>/written/', views.enter_written_grades, name='enter_written_grades'),
    path('exam/<int:exam_id>/oral/', views.enter_oral_grades, name='enter_oral_grades'),
    path('exam/<int:exam_id>/finalize/', views.finalize_exam, name='finalize_exam'),
    path('exams/finalized/', views.finalized_exam_list, name='finalized_exam_list'),
    path('exam/<int:exam_id>/reopen/', views.reopen_exam, name='reopen_exam'),

    # ============================================================
    # 6. STAFF PANEL
    # ============================================================
    path('staff/enrollment/', views.staff_enrollment, name='staff_enrollment'),
    path('staff/students/', views.staff_student_profiles, name='staff_student_profiles'),
    path('staff/finance/', views.staff_finance, name='staff_finance'),

    # ============================================================
    # 7. MANAGER PANEL (Education & Senior)
    # ============================================================
    path('manager/classes/', views.manage_classes, name='manage_classes'),
    path('manager/courses/', views.manage_courses, name='manage_courses'),
    path('manager/teachers/', views.manage_teachers, name='manage_teachers'),
    path('manager/reports/', views.manager_reports, name='manager_reports'),
    path('manager/finance/', views.finance_reports, name='finance_reports'),
    path('class/create/', views.create_class, name='create_class'),
    path('course/create/', views.create_course, name='create_course'),
    path('placement/settings/', views.placement_test_settings, name='placement_test_settings'),
    path('placement/requests/', views.manage_placement_requests, name='manage_placement_requests'),
    path('placement/request/<int:request_id>/review/', views.review_placement_request, name='review_placement_request'),
    
    # --- Teacher Quick Actions (inside manager) ---
    path('teacher/create/', views.create_teacher, name='create_teacher'),
    path('teacher/<int:teacher_id>/quick-edit/', views.quick_edit_teacher, name='quick_edit_teacher'),
    path('teacher/<int:teacher_id>/profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher/<int:teacher_id>/classes/', views.teacher_assign_classes, name='teacher_assign_classes'),
    path('class/<int:class_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('teacher/performance/', views.teacher_performance, name='teacher_performance'),

    # --- User Management (Senior Manager only) ---
    path('manager/users/', views.user_management, name='user_management'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/<int:user_id>/manage/', views.manage_user, name='manage_user'),
    path('user/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),

    # ============================================================
    # 8. PAYMENTS & INVOICES
    # ============================================================
    path('class/<int:class_id>/payment/', views.mock_payment, name='mock_payment'),
    path('invoice/<int:invoice_id>/pay/', views.pay_invoice, name='pay_invoice'),
    path('invoice/<int:invoice_id>/receipt/', views.invoice_receipt, name='invoice_receipt'),
    path('placement/pay/<int:request_id>/', views.pay_placement_test, name='pay_placement_test'),

    # ============================================================
    # 9. MISC & FALLBACK
    # ============================================================
    path('error-test/', lambda request: render(request, 'base/error.html', {'message': 'Test message'})),
    path('', lambda request: redirect('dashboard'), name="home"),
]