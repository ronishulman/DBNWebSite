from django import forms
from django.forms import ModelForm
from .models import WorkSchedule
from employee.models import Employee
from clients.models import Client

TYPE_OF_SHIFT_CHOICES = [
    ('', '---------'),
    ('הקמה', 'הקמה'),
    ('פירוק', 'פירוק'),
    ('נציגות', 'נציגות'),
    ('פירוק + פריקה במחסן', 'פירוק + פריקה במחסן'),
    ('ראש צוות', 'ראש צוות'),
]

class WorkScheduleForm(ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label=None, label='לקוח', widget=forms.Select(attrs={'class': 'full-width'}))
    type_of_shift = forms.ChoiceField(choices=TYPE_OF_SHIFT_CHOICES, label='סוג משמרת', widget=forms.Select(attrs={'class': 'full-width'}))

    class Meta:
        model = WorkSchedule
        fields = ['date', 'day', 'beginning_time', 'client', 'type_of_shift', 'num_of_employees', 'name_of_employees', 'location','notes']

        labels = {
            'date': 'תאריך',
            'day': 'יום',
            'type_of_shift':'סוג משמרת',
            'beginning_time': 'שעת התחלה',
            'client': 'לקוח',
            'num_of_employees': 'מספר עובדים',
            'name_of_employees': 'שם העובדים',
            'location': 'מיקום',
            'notes': 'הערות',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'full-width'}),
            'day': forms.TextInput(attrs={'class': 'form-control'}),
            'beginning_time': forms.TimeInput(attrs={'type': 'time', 'class': 'full-width'}),
            'num_of_employees': forms.TextInput(attrs={'class': 'form-control'}),
            'name_of_employees': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class WorkScheduleForm(ModelForm):
#     client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label=None, label='לקוח', widget=forms.Select(attrs={'class': 'full-width'}))
#     type_of_shift = forms.ChoiceField(choices=TYPE_OF_SHIFT_CHOICES, label='סוג משמרת', widget=forms.Select(attrs={'class': 'full-width'}))
#     name_of_employees = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), label='שם העובדים', widget=forms.CheckboxSelectMultiple)

#     class Meta:
#         model = WorkSchedule
#         fields = ['date', 'day', 'beginning_time', 'client', 'type_of_shift', 'num_of_employees', 'name_of_employees', 'location', 'notes']

#         labels = {
#             'date': 'תאריך',
#             'day': 'יום',
#             'type_of_shift': 'סוג משמרת',
#             'beginning_time': 'שעת התחלה',
#             'client': 'לקוח',
#             'num_of_employees': 'מספר עובדים',
#             'name_of_employees': 'שם העובדים',
#             'location': 'מיקום',
#             'notes': 'הערות',
#         }
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'full-width'}),
#             'day': forms.TextInput(attrs={'class': 'form-control'}),
#             'beginning_time': forms.TimeInput(attrs={'type': 'time', 'class': 'full-width'}),
#             'num_of_employees': forms.TextInput(attrs={'class': 'form-control'}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'notes': forms.TextInput(attrs={'class': 'form-control'}),
#         }
