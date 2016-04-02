from django.contrib import admin

from .models import Secret, SecretGroup, UserDevice

admin.site.register(Secret)
admin.site.register(SecretGroup)
admin.site.register(UserDevice)
