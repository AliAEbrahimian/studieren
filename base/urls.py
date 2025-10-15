from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('myprofile/', views.myProfile, name="myprofile"),
    path('editprofile/', views.editProfile, name="editprofile"),
    path('resetpassword/', views.resetPasswordRequest, name="resetpassword"),
    path('resetpassword/<uidb64>/<token>/', views.resetPasswordConfirm, name="resetpasswordconfirm"),
    
    path('', views.home , name="home"),
    
    path('room/<int:pk>/', views.room , name="room"),
    
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]