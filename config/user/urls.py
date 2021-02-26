from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import *
from .forms import *

#namespace
app_name = 'user'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', form_class=UserLoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'), name="logout"),
    path('signup/', signup, name="signup"),

    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),

    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),

    #password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password/password_reset.html",
                                                                success_url=reverse_lazy('user:password_reset_done'),
                                                                email_template_name='password/password_reset_email.html',
                                                                form_class=PasswordResetForm,
                                                                subject_template_name="password/password_reset_email_title.html"), 
                                                                name='password_reset'),
    path('password_reset/password_reset_done/', TemplateView.as_view(template_name="password/password_reset_done.html"), name='password_reset_done'),


    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html',
                                                                                                success_url=reverse_lazy('user:password_reset_sussess'),
                                                                                                form_class=PasswordResetConfirmForm),
                                                                                                name="password_reset_confirm"),
    
    path('password_reset_confirm/password_reset_complete/', TemplateView.as_view(template_name="password/password_reset_success.html"), name='password_reset_sussess'),
]