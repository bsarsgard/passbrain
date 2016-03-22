from __future__ import unicode_literals

#from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device_id = models.CharField(max_length=1024)
    device_name = models.CharField(max_length=100)
    public_key = models.TextField()

class SecretGroup(models.Model):
    label = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

class SecretValue(models.Model):
    secret = models.ForeignKey('Secret')
    userdevice = models.ForeignKey('UserDevice')
    value = models.TextField()

class Secret(models.Model):
    label = models.CharField(max_length=100)
    groups = models.ManyToManyField('SecretGroup')
