from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Pet, Reminder


# ======================================
# USER REGISTRATION FORM (FIXED)
# ======================================

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ======================================
# USER LOGIN FORM (OK)
# ======================================

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# ======================================
# PET FORM (ADMIN USE)
# ======================================

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name',
            'breed',
            'pet_type',
            'age',
            'description',
            'health_status',
            'image',
            'status'
        ]


# ======================================
# REMINDER FORM (OPTIONAL)
# ======================================

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = [
            'title',
            'description',
            'reminder_type',
            'pet',
            'reminder_date',
            'reminder_time',
            'is_recurring'
        ]
        widgets = {
            'reminder_date': forms.DateInput(attrs={'type': 'date'}),
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }
