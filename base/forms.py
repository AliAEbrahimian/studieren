from django.forms import ModelForm
from .models import Room
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount
from django import forms

class RoomForm (ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
class RegisterForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username',
                  'first_name',
                  'last_name',
                  'birthday',
                  'email',
                  'phone',
                  'address',
                  'postcode',
                  'password1',
                  'password2']
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date'
            })
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = {'first_name',
                  'last_name',
                  'birthday',
                  'email',
                  'phone',
                  'address',
                  'postcode'}
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date',
            })
        }
