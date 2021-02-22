from django.shortcuts import render, redirect
from .forms import *
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            auth.login(request, login_form.get_user())
            return redirect('store:product_all')
        else:

            return render(request, 'login/login.html',  {
            'form': form,
        })
    else:
        return render(request, 'login/login.html', {'form': UserLoginForm()})

def logout(request):
    pass
