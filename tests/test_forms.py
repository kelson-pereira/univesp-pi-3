from django.test import TestCase
from plantio.forms import *

def test_login_form_valid_data():
    form = LoginForm(data={
        'email': 'usuario@exemplo.com',
        'password': 'senhasegura123'
    })
    assert form.is_valid()


def test_login_form_empty_fields():
    form = LoginForm(data={
        'email': '',
        'password': ''
    })
    assert not form.is_valid()
    assert 'email' in form.errors
    assert 'password' in form.errors


def test_login_form_invalid_email_format():
    form = LoginForm(data={
        'email': 'nao-e-mail',
        'password': '123456'
    })
    assert not form.is_valid()
    assert 'email' in form.errors