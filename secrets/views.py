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
from .models import SecretValue
from .permissions import IsUserOrReadOnly
from .serializers import UserDeviceSerializer
from .serializers import UserSerializer
from .serializers import SecretSerializer
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
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)

class SecretValueViewSet(viewsets.ModelViewSet):
    queryset = SecretValue.objects.all()
    serializer_class = SecretValueSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
            IsUserOrReadOnly,)
