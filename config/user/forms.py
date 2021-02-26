
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)

from .models import User

def clean_password(password):

    vali_data = [
            lambda s: any(x.islower() for x in s), #소문자 하나이상
            lambda s: any(x.isdigit() for x in s), #숫자 하나이상
            lambda s: len(s) == len(s.replace(" ", "")), #스페이스 거름
            lambda s: len(s) >= 7  #7자 미만 안댐
            ]
    for data in vali_data:
        if not data(password):
            return False
            
    return True

class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, error_messages={
        'required': 'Sorry, you will need an email'})

    username = forms.CharField(min_length=2, max_length=255)

    first_name = forms.CharField(max_length=255, required = False)

    last_name = forms.CharField(max_length=255, required = False)

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        else:
            if not clean_password(cd['password2']):
                raise forms.ValidationError("It doesn't fit the form")
            # vali_data = [
            # lambda s: any(x.islower() for x in s), #소문자 하나이상
            # lambda s: any(x.isdigit() for x in s), #숫자 하나이상
            # lambda s: len(s) == len(s.replace(" ", "")), #스페이스 거름
            # lambda s: len(s) >= 7  #7자 미만 안댐
            # ]
            # for data in vali_data:
            #     if not data(cd['password2']):
            #         raise forms.ValidationError("It doesn't fit the form")

        return cd['password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username (Required)' })
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'email@email.com (Required)', 'name': 'email', 'id': 'id_email'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Last Name'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password (Required)'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password (Required)'})


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
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


class UserProfileForm(forms.ModelForm):
    # email = forms.EmailField(
    #     label='Account email (can not be changed)', max_length=255, widget=forms.TextInput(
    #         attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label='Username', min_length=2, max_length=255, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username'}))
    
    first_name = forms.CharField(
        label='Username', max_length=255, required = False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Username', max_length=255, required = False, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name', 'id': 'form-lastname'}))


    class Meta:
        model = User
        fields = ['email','username','first_name','last_name']

    #front에서 email 수정 방지
    def clean_email(self):
        return self.instance.email

    def clean_username(self):
        username = self.cleaned_data['username']

        if self.instance.username != username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'email@email.com (Required)', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email

class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-password1'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Repeat password', 'id': 'form-password2'}))

