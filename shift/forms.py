from django import forms
from django.forms import ModelForm
from shift.models import Shift
from clients.models import Client

TYPE_OF_SHIFT_CHOICES = [
    ('', '---------'),
    ('הקמה', 'הקמה'),
    ('פירוק', 'פירוק'),
    ('נציגות', 'נציגות'),
    ('פירוק + פריקה במחסן', 'פירוק + פריקה במחסן'),
    ('ראש צוות', 'ראש צוות'),
]

TYPE_OF_CLIENTS = [
    ('', '---------'),
    ('אלון חסון', 'אלון חסון'),
    ('סקיי', 'סקיי'),
    ('מירו', 'מירו'),
]

all_clients = Client.objects.all()

# Create a list of choices for clients
client_choices = [('', '---------')]  # Initial empty option
client_choices.extend([(client.name, str(client)) for client in all_clients])

class ShiftFillingForm(ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="", label='לקוח')
    type_of_shift = forms.ChoiceField(choices=TYPE_OF_SHIFT_CHOICES, label='סוג משמרת')
    
   
    class Meta:
        model = Shift
        fields = ['client', 'type_of_shift', 'location']
           
        labels = {
            'client': 'לקוח',
            'type_of_shift': 'סוג משמרת',
            'location': 'מיקום',
            'amount_of_km': 'כמות קילומטרים',
            'public_transport': 'תחבורה ציבורית',
            'food': 'אוכל',
            'parking_refund': 'החזר חניה',
        }
        widgets = {
                'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'מיקום', 'required': False}),
                'amount_of_km': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
                'public_transport': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
                'food': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
                'parking_refund': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        }

class ShiftUpdateForm(ModelForm):
    # client = forms.ModelChoiceField(queryset=Client.objects.all(), label='לקוח')
    client = forms.ChoiceField(choices=client_choices, label='לקוח')
    type_of_shift = forms.ChoiceField(choices=TYPE_OF_SHIFT_CHOICES, label='סוג משמרת')
    amount_of_km = forms.FloatField(label='כמות קילומטרים', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    public_transport = forms.FloatField(label='תשלום על תחבורה ציבורית', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    food = forms.FloatField(label='תשלום על אוכל', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parking_refund = forms.FloatField(label='תשלום על חנייה', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
   
    class Meta:
        model = Shift
        fields = ['shift_start_date_time', 'shift_end_date_time', 'type_of_shift', 'client', 'location', 'amount_of_km', 'public_transport', 'food', 'parking_refund']

        labels = {
            'shift_start_date_time': 'תאריך ושעת תחילת משמרת',
            'shift_end_date_time': 'תאריך ושעת סוף משמרת',
            'client': 'לקוח',
            'type_of_shift': 'סוג משמרת',
            'location': 'מיקום',
            'amount_of_km': 'כמות קילומטרים',
            'public_transport': 'תחבורה ציבורית',
            'food': 'אוכל',
            'parking_refund': 'החזר חניה',
        }
        widgets = {
                'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'מיקום'}),
                # 'client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'לקוח'}),
                'shift_start_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
                'shift_end_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

        