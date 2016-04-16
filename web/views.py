from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from secrets.decorators import device_required
from secrets.models import Secret
from secrets.models import SecretGroup
from secrets.models import SecretValue
from secrets.models import UserDevice
from .forms import ProfileForm
from .forms import SecretForm
from .forms import UserDeviceForm


"""
Public areas
"""


def index(request):
    template = loader.get_template('web/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def error(request):
    return render(request, 'web/error.html')


"""
Protected areas
"""


@login_required
@device_required
def sandbox(request, device):
    return render(request, 'web/sandbox.html',
            {'device': device})


@login_required
@device_required
@ensure_csrf_cookie
def profile(request, device):
    if not request.user.email:
        request.user.email = request.user.username
        request.user.save()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    userdevices = UserDevice.objects.filter(user=request.user)
    secrets = Secret.objects.filter(values__userdevice__user=request.user)
    groups = SecretGroup.objects.filter(users=request.user)

    response = render(request, 'web/profile.html',
            {'form': form, 'device': device, 'userdevices': userdevices,
            'secrets': secrets, 'groups': groups},)
    response.set_cookie('device_id', device.id, max_age=365*24*60*60)
    return response


@login_required
def device(request):
    if request.method == 'POST':
        form = UserDeviceForm(request.POST)
        if form.is_valid():
            device = UserDevice(user=request.user,
                    agent=request.META.get('HTTP_USER_AGENT', ''),
                    ip_address = request.META.get('REMOTE_ADDR', ''),
                    name=form.cleaned_data['name'],
                    public_key=form.cleaned_data['public_key'],
                    is_authorized=False, is_active=True)
            if not SecretGroup.objects.filter(users=request.user).exists():
                # If there are no groups, we auto-authorize this record and
                # create a self group. We can't do this if there are any groups
                # because they might have secrets.
                group = SecretGroup(label='Self', is_default=True,
                        is_hidden=True, is_active=True)
                group.save()
                group.users.add(request.user)
                device.is_authorized = True
            device.save()
            response = redirect('profile')
            response.set_cookie('device_id', device.id, max_age=365*24*60*60)
            return response
        device = None
        return render(request, 'web/device.html',
                {'form': form, 'device': device})
    else:
        try:
            device = UserDevice.objects.get(user=request.user,
                    pk=request.COOKIES.get('device_id', 0),
                    is_active=True)
        except:
            device = None
        form = UserDeviceForm()
        return render(request, 'web/device.html',
                {'form': form, 'device': device})


@login_required
def device_read(request, device_id):
    try:
        device = UserDevice.objects.get(user=request.user,
                pk=device_id,
                is_active=True)
        response = redirect('profile')
        response.set_cookie('device_id', device.id, max_age=365*24*60*60)
        return response
    except:
        return redirect('device')


@login_required
@device_required
def dashboard(request, device):
    template = loader.get_template('web/dashboard.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


@login_required
@device_required
@ensure_csrf_cookie
def secrets(request, device):
    secrets = Secret.objects.filter(groups__users=request.user)
    """
    secretvalues = SecretValue.objects.filter(userdevice=device,
            secret__groups__users=request.user)
    """
    return render(request, 'web/secrets.html',
            {'secrets': secrets, 'device': device})


@login_required
@device_required
def secret_create(request, device):
    form = SecretForm(user=request.user)
    return render(request, 'web/secret_create.html',
            {'form': form, 'device': device})


@login_required
@device_required
def secret_read(request, secret_id, device):
    secret = get_object_or_404(Secret, pk=secret_id)
    secretvalue = SecretValue.objects.filter(secret=secret,
                userdevice=device,
                is_active=True).order_by('-created')[0]
    return render(request, 'web/secret_read.html',
            {'secret': secret, 'device': device, 'secretvalue': secretvalue})


@login_required
@device_required
def secret_update(request, secret_id, device):
    secret = get_object_or_404(Secret, pk=secret_id)
    secretvalue = SecretValue.objects.filter(secret=secret,
                userdevice=device,
                is_active=True).order_by('-created')[0]
    form = SecretForm(user=request.user, initial={'label': secret.label,
            'value': '[ Decrypting, please wait ]'})
    return render(request, 'web/secret_update.html',
            {'form': form, 'secret': secret, 'device': device,
                    'secretvalue': secretvalue})


@login_required
@device_required
def secret_delete(request, secret_id, device):
    return render(request, 'web/secret_delete.html')
