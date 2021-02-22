
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import User



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'email@email.com', 'id': 'login-email'}))
        
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mb',
            'placeholder': 'Password',
            'id': 'login-password',
        }
    ))

    error_messages = {
        'invalid_login': (
            "비밀번호나 이메일이 올바르지 않습니다. 다시 확인해 주세요."
        ),
        'inactive': ("이 계정은 인증되지 않았습니다. 인증을 먼저 진행해 주세요."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs) # 꼭 있어야 한다!
        self.fields['username'].label = 'email'
        self.fields['password'].label = 'password'
