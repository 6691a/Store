from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .forms import *

#namespace
app_name = 'user'
urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html',form_class=UserLoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'), name="logout"),


]