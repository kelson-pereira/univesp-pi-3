from django import forms

class LoginForm(forms.Form):
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'Seu email aqui',
    'required': 'required'
  }))
  password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
    'class': 'form-control',
    'placeholder': 'Sua senha aqui',
    'required': 'required'
  }))

class SignupForm(forms.Form):
  first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={
      'class': 'form-control',
      'placeholder': 'Nome'
  }))
  last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={
      'class': 'form-control',
      'placeholder': 'Sobrenome'
  }))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
      'class': 'form-control',
      'placeholder': 'Email'
  }))
  password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
      'class': 'form-control',
      'placeholder': 'Senha'
  }))
