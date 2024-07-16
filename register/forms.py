from django import forms
from django.forms import ModelForm
from .models import EmployeesWaitingForApproval

class SingUpForm(ModelForm):

    class Meta:
        model = EmployeesWaitingForApproval
        fields = ['user_name', 'first_name', 'last_name', 'id', 'email', 'pass1', 'pass2']

        labels = {
            'user_name': 'שם משתמש',
            'first_name': 'שם פרטי',
            'last_name':'שם משפחה',
            'id': 'תעודת זהות',
            'email': 'אימייל',
            'pass1': 'סיסמא',
            'pass2': 'חזור על הסיסמא',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'type': 'date', 'class': 'full-width'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TimeInput(attrs={'type': 'time', 'class': 'full-width'}),
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'pass1': forms.TextInput(attrs={'class': 'form-control'}),
            'pass1': forms.TextInput(attrs={'class': 'form-control'}),
        }