from django.contrib import admin

from .models import Secret, SecretValue, SecretGroup, UserDevice

admin.site.register(Secret)
admin.site.register(SecretValue)
admin.site.register(SecretGroup)
admin.site.register(UserDevice)
