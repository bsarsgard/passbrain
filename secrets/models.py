from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

"""
UserDevice - this represents a browser that is able to access secrets on behalf
of a user
"""
class UserDevice(models.Model):
    user = models.ForeignKey('auth.User', related_name='devices')
    agent = models.CharField(max_length=1024)
    ip_address = models.GenericIPAddressField()
    name = models.CharField(max_length=100)
    public_key = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s: %s" % (self.user.__unicode__(), self.name)


"""
SecretGroup - Secrets are shared between users via groups, or tracked
internelly with special default and hidden groups. A secret that is linked to a
user via a group will be trackable for updates, whereas an orphaned link will
not be updated and should be hidden.
"""
class SecretGroup(models.Model):
    label = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='secretgroups')
    is_default = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.label


"""
SecretValue - This is where the actual encrypted passwords or other secret data
are stored. These will be unique to each device, with an AES key and iv
encrypted with the UserDevice's public key, and are in turn used to decrpt the
encrypted value.
"""
class SecretValue(models.Model):
    secret = models.ForeignKey('Secret', related_name='values')
    userdevice = models.ForeignKey('UserDevice')
    encrypted_key = models.CharField(max_length=1024)
    encrypted_iv = models.CharField(max_length=1024)
    encrypted_value = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s (%s)" % (self.secret.__unicode__(),
                self.userdevice.__unicode__())


"""
Secret - Represents a secret entity which will be distributed among users and
encrypted in their own SecretValue records (where the actual data is stored).
"""
class Secret(models.Model):
    label = models.CharField(max_length=100)
    groups = models.ManyToManyField('SecretGroup', related_name='secrets')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.label

    @property
    def users(self):
        return User.objects.filter(secretgroups__secrets=self)
