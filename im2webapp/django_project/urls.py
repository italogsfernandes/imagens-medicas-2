from django.contrib import admin
from django.urls import path, include
from users.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', include('im2webapp.urls')),
]
