from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from secrets import views


router = DefaultRouter()
router.register(r'userdevices', views.UserDeviceViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'secrets', views.SecretViewSet)
router.register(r'secretgroups', views.SecretGroupViewSet)
router.register(r'secretvalues', views.SecretValueViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
