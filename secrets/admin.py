from django.contrib import admin

from .models import Secret, SecretValue, SecretGroup, Trust, TrustUser, UserDevice

class TrustUserAdmin(admin.TabularInline):
    model = TrustUser
    extra = 2

class TrustAdmin(admin.ModelAdmin):
    inlines = (TrustUserAdmin,)

admin.site.register(Secret)
admin.site.register(SecretValue)
admin.site.register(SecretGroup)
admin.site.register(Trust, TrustAdmin)
admin.site.register(UserDevice)
