from __future__ import unicode_literals

from django.conf import settings
from django.db import models

class UserDevice(models.Model):
    user = models.ForeignKey('auth.User', related_name='devices')
    agent = models.CharField(max_length=1024)
    name = models.CharField(max_length=100)
    public_key = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class SecretGroup(models.Model):
    label = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='secretgroups')

class SecretValue(models.Model):
    secret = models.ForeignKey('Secret', related_name='values')
    userdevice = models.ForeignKey('UserDevice')
    encrypted_key = models.CharField(max_length=1024)
    encrypted_iv = models.CharField(max_length=1024)
    encrypted_value = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Secret(models.Model):
    label = models.CharField(max_length=100)
    groups = models.ManyToManyField('SecretGroup')
    created = models.DateTimeField(auto_now_add=True)
