from django import forms
from .models import Energy
from django.contrib.auth.forms import AuthenticationForm


# EnergyForm is a ModelForm, which is a helper class that lets you create a Form class from a Django model.
class EnergyForm(forms.ModelForm):
    class Meta:
        # The model to be used is 'Energy'
        model = Energy
        # The model fields to be included in the form
        fields = ['produced_energy_in_watt', 'consumed_energy_in_watt']


# CustomAuthenticationForm is a form for authenticating users. Extends Django's AuthenticationForm.
class CustomAuthenticationForm(AuthenticationForm):
    # Custom error messages
    error_messages = {
        # 'invalid_login' error message
        'invalid_login': "Incorrect username or password.",
        # 'inactive' error message
        'inactive': "This account is inactive.",
    }


# FileUploadForm is a form for uploading files
class FileUploadForm(forms.Form):
    # file field
    file = forms.FileField()
