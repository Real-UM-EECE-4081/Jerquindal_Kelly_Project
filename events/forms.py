from django import forms
from django.forms import ModelForm
from .models import TrainingSite, Event


# Admin SuperUser Event Form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'site', 'manager', 'volunteers', 'description')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'site': 'Training Site',
            'manager': 'Manager',
            'volunteers': 'Volunteers',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'site': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Training Site'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'volunteers': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Volunteers'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# User Event Form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'site', 'volunteers', 'description')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'site': 'Training Site',
            'volunteers': 'Volunteers',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'site': forms.Select(attrs={'class': 'form-select', 'placeholder': 'TrainingSite'}),
            'volunteers': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Volunteers'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# Create a site form
class TrainingSiteForm(ModelForm):
    class Meta:
        model = TrainingSite
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'site_image')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'site_image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training Site'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web Address'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
