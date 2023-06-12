from django import forms
from .models import Energy
from django.contrib.auth.forms import AuthenticationForm


class EnergyForm(forms.ModelForm):
    class Meta:
        model = Energy
        fields = ['produced_energy_in_watt', 'consumed_energy_in_watt']


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Username o password errati.",
        'inactive': "Questo account è inattivo.",
    }


class FileUploadForm(forms.Form):
    file = forms.FileField()
