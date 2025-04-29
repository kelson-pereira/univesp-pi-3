from django import forms

class LoginForm(forms.Form):
  email = forms.EmailField(widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'Seu email aqui',
    'required': 'required'
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Sua senha aqui',
    'required': 'required'
  }))