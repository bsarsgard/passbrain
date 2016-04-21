from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^error/$', views.error, name='error'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^sandbox/$', views.sandbox, name='sandbox'),
    url(r'^device/$', views.device, name='device'),
    url(r'^device/(?P<device_id>[0-9]+)$$', views.device_read,
            name='device_read'),
    url(r'^secrets/$', views.secrets, name='secrets'),
    url(r'^secret/$', views.secret_create, name='secret_create'),
    url(r'^secret/(?P<secret_id>[0-9]+)/$', views.secret_read,
             name='secret_read'),
    url(r'^secret/(?P<secret_id>[0-9]+)/update/$', views.secret_update,
             name='secret_update'),
    url(r'^secret/(?P<secret_id>[0-9]+)/delete/$', views.secret_delete,
             name='secret_delete'),
    url(r'^trust/(?P<trust_id>[0-9]+)/$', views.trust_read,
             name='trust_read'),
]
