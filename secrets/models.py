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
Trust - A collection of groups with set administrators
"""
class Trust(models.Model):
    label = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
            through='TrustUser', related_name='trusts')

    def __unicode__(self):
        return self.label


class TrustUser(models.Model):
    trust = models.ForeignKey('Trust')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
            related_name='trustusers')
    is_admin = models.BooleanField(default=False)

    def get_status(self):
        return 'success' if self.is_admin else 'primary'


"""
SecretGroup - Secrets are shared between users via groups, or tracked
internelly with special default and hidden groups. A secret that is linked to a
user via a group will be trackable for updates, whereas an orphaned link will
not be updated and should be hidden.
Groups may be within trusts, or may be private groups between users. All users
have a default 'Self' group that is hidden, and users sharing passwords
between themselves directly can create hidden groups to do so.
If a trust is specified, all admins will automatically be added to it.
"""
class SecretGroup(models.Model):
    label = models.CharField(max_length=100)
    trust = models.ForeignKey('Trust', null=True, blank=True,
            related_name='secretgroups')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
            related_name='secretgroups')
    is_default = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.label

    def get_status(self):
        if not self.is_active:
            return 'danger'
        elif self.is_default:
            return 'default'
        elif self.is_hidden:
            return 'warning'
        else:
            return 'primary'


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
Message - A holder for a secret shared directly instead of using group access
This is important since changing group access should never retroactively
reveal or hide massages that were sent in the past.
"""
class SecretMessage(models.Model):
    secret = models.ForeignKey('Secret')
    sender = models.ForeignKey('auth.User')
    recipients = models.ManyToManyField('auth.User', related_name='messages')

    def __unicode__(self):
        return self.secret.label


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


"""
Notification - notify users of changes or newly added items
"""
class Notification(models.Model):
    MESSAGE = 'ME'
    NOTIFICATION = 'NO'
    ALERT = 'AL'
    NOTIFICATION_TYPE_CHOICES = (
        (MESSAGE, 'Message'),
        (NOTIFICATION, 'Notification'),
        (ALERT, 'Alert'),
    )

    user = models.ForeignKey('auth.User')
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    relative_url = models.CharField(max_length=1024)
    notification_type = models.CharField(max_length=2,
        choices=NOTIFICATION_TYPE_CHOICES, default=NOTIFICATION)
    created = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    is_done = models.BooleanField(default=True)
