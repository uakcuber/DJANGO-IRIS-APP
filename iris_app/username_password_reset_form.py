from django import forms
from django.contrib.auth.models import User

class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(
        label="Kullanıcı Adı",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı adınızı girin'
        })
    )
