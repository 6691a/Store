from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from impOrder.views import user_orders 
from .forms import *
from .token import account_activation_token
from .models import User



def login(request):
    next = request.GET.get("next", None)
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
       
        if form.is_valid():
            auth.login(request, login_form.get_user())
            if next is not None:
                return redirect(next)
            else:
                return redirect('store:product_all')
        else:
            return render(request, 'login/login.html',  {
            'form': form,
        })
    else:
            return render(request, 'login/login.html', {'form': UserLoginForm()})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        signupForm = CreateUserForm(request.POST)
        if signupForm.is_valid():
            ''' 내부적으로 구현되어 있음 (멤버변수 인스턴스)
		    향후 수정 기능 구현시 활용 '''
            user = signupForm.save(commit=False)
            user.email = signupForm.cleaned_data['email']
            user.set_password(signupForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            #Setup email
            current_site = get_current_site(request)
            title = '[Stay Gold] Activate your Account'
            message = render_to_string('activation/activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(title, message, to=[user.email])
            email.send()
            return render(request,'signup/signup_success.html', {'email':user.email})
    else:
        signupForm = CreateUserForm()

    return render(request,'signup/signup.html',{'form': signupForm})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'activation/activation_invalid.html')

@login_required
def profile(request):
    if request.method == 'POST':

        form = UserProfileForm(instance=request.user, data=request.POST)
        print(form)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile/profile.html', {'form': form})

@login_required
def dashboard(request):
    orders = user_orders(request)
    # print(orders.objects.all())
    return render(request, 'dashboard/dashboard.html', {'orders': orders})
