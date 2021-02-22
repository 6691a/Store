from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include('user.urls',namespace='user')),
    path('cart/', include('cart.urls',namespace='cart')),

    path('summernote/', include('django_summernote.urls')),
    path('', include('store.urls', namespace='store')),
]
