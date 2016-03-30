from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from secrets.models import UserDevice
from secrets.permissions import IsUserOrReadOnly
from secrets.serializers import UserDeviceSerializer
from secrets.serializers import UserSerializer


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
