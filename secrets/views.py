from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import UserDevice
from .models import Secret
from .models import SecretGroup
from .models import SecretValue
from .permissions import IsUserOrReadOnly
from .permissions import ReadIfUserInUsers
from .serializers import UserDeviceSerializer
from .serializers import UserSerializer
from .serializers import SecretSerializer
from .serializers import SecretGroupSerializer
from .serializers import SecretValueSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'userdevices': reverse('userdevice-list', request=request,
                format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeviceViewSet(viewsets.ModelViewSet):
    queryset = UserDevice.objects.all()
    serializer_class = UserDeviceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly,)
    filter_fields = ('user',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    permission_classes = (ReadIfUserInUsers,)

    def get_queryset(self):
        return Secret.objects.filter(groups__users=self.request.user)


class SecretValueViewSet(viewsets.ModelViewSet):
    queryset = SecretValue.objects.all().order_by('-created')
    serializer_class = SecretValueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly,)
    filter_fields = ('secret','userdevice')

class SecretGroupViewSet(viewsets.ModelViewSet):
    queryset = SecretGroup.objects.all()
    serializer_class = SecretGroupSerializer
    permission_classes = (ReadIfUserInUsers,)
    filter_fields = ('is_default','is_hidden')

    def get_queryset(self):
        return SecretGroup.objects.filter(users=self.request.user)
