"""passbrain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    url(r'^', include('web.urls')),
    url(r'^register/', CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/dashboard'), name='register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^api/', include('secrets.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
             namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]
