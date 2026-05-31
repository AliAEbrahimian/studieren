from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import Room
from .models import UserAccount
from django.core.validators import RegexValidator

class RoomForm (ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+$',
                message='Only letters of the alphabet. For exaample: Alice'
            ),
        ],
        required=True
    )
    
    last_name = forms.CharField(
        max_length=30,
        validators=[RegexValidator(
            regex=r'^[A-Za-z]+$',
            message='Only letters of the alphabet. For exaample: Jakson'
            )
        ],
        required=True
    )
    
    phone = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09[0-9]{9}$',
                message='For example: 09121234567'
            )
        ],
        required=True
    )
    
    postal_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Postal code must be exactly 10 digits.'
            )
        ]
    )
    
    national_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='The national code must be exactly 10 digits.'
            )
        ]
    )
    
    gender = forms.ChoiceField(
        choices=UserAccount.GENDER_CHOICES,
        required=False,
        widget=forms.RadioSelect
        )
    
    emergency_contact = forms.CharField(
        max_length=11,
        required=False
    )
    
    city = forms.CharField(
        max_length=25,
        required=False
    )
    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'birthday', 'email', 'phone', 'address', 'postal_code',
                  'national_code', 'gender', 'emergency_contact', 'city']
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date'
            })
        }

class UserUpdateForm(forms.ModelForm):
    
    first_name = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+$',
                message='Only letters of the alphabet. For exaample: Alice'
            ),
        ],
        required=True
    )
    
    last_name = forms.CharField(
        max_length=30,
        validators=[RegexValidator(
            regex=r'^[A-Za-z]+$',
            message='Only letters of the alphabet. For exaample: Jakson'
            )
        ],
        required=True
    )
    
    phone = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09[0-9]{9}$',
                message='For example: 09121234567'
            )
        ],
        required=True
    )
    
    postal_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Postal code must be exactly 10 digits.'
            )
        ]
    )
    
    national_code = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='The national code must be exactly 10 digits.'
            )
        ]
    )
    
    gender = forms.ChoiceField(
        choices=UserAccount.GENDER_CHOICES,
        required=False,
        widget=forms.RadioSelect
        )
    
    emergency_contact = forms.CharField(
        max_length=11,
        required=False
    )
    
    city = forms.CharField(
        max_length=25,
        required=False
    )
    
    bio = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = UserAccount
        fields = ['first_name','last_name','birthday','email','phone','address','postal_code',
                  'national_code', 'gender', 'emergency_contact', 'city']
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date',
            })
        }
