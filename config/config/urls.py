from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('cart/', include('cart.urls',namespace='cart')),
    path('', include('store.urls', namespace='store')),
]
