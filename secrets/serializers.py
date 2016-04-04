from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserDevice
from .models import Secret
from .models import SecretValue


class UserSerializer(serializers.HyperlinkedModelSerializer):
    devices = serializers.HyperlinkedRelatedField(many=True,
            view_name='userdevice-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'devices')


class UserDeviceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserDevice
        fields = ('id', 'url', 'user', 'agent', 'name', 'public_key',
                'created', 'is_authorized', 'is_active')


class SecretSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Secret
        fields = ('id', 'url', 'label',)


class SecretValueSerializer(serializers.HyperlinkedModelSerializer):
    secret = serializers.HyperlinkedRelatedField(
            view_name='secret-detail', queryset=Secret.objects.all())
    userdevice = serializers.HyperlinkedRelatedField(
            view_name='userdevice-detail', queryset=UserDevice.objects.all())

    class Meta:
        model = SecretValue
        fields = ('id', 'url', 'encrypted_key', 'encrypted_iv',
                 'encrypted_value', 'created', 'is_active', 'secret',
                 'userdevice')
