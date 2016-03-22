from django.contrib import admin

from .models import Secret, SecretGroup

admin.site.register(Secret)
admin.site.register(SecretGroup)
