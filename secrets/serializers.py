from django.contrib.auth.models import User
from rest_framework import serializers

from models import UserDevice


class UserSerializer(serializers.HyperlinkedModelSerializer):
    devices = serializers.HyperlinkedRelatedField(many=True,
            view_name='userdevice-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'devices')


class UserDeviceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserDevice
        fields = ('url', 'user', 'device_id', 'device_name', 'public_key',
                'created', 'is_authorized', 'is_active')
