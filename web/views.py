from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import ensure_csrf_cookie

from secrets.models import Secret
from secrets.models import SecretValue
from secrets.models import UserDevice
from .forms import UserDeviceForm, SecretForm

def index(request):
    template = loader.get_template('web/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def error(request):
    return render(request, 'web/error.html')

@login_required
def sandbox(request):
    device = None
    try:
        device = UserDevice.objects.get(user=request.user,
                agent=request.META.get('HTTP_USER_AGENT', ''),
                is_authorized=True,
                is_active=True)
    except:
        return redirect('device')
    return render(request, 'web/sandbox.html',
            {'device': device})

@login_required
def device(request):
    if request.method == 'POST':
        form = UserDeviceForm(request.POST)
        if form.is_valid():
            device = UserDevice(user=request.user,
                    agent=request.META.get('HTTP_USER_AGENT', ''),
                    name=form.cleaned_data['name'],
                    public_key=form.cleaned_data['public_key'],
                    is_active=True)
            if UserDevice.objects.filter(user=request.user,
                    is_active=True).exists():
                device.save()
                return redirect('device')
            else:
                # the first device authorizes "free"
                device.is_authorized = True
                device.save()
                return redirect('sandbox')
        device = None
        return render(request, 'web/device.html',
                {'form': form, 'device': device})
    else:
        try:
            device = UserDevice.objects.get(user=request.user,
                    agent=request.META.get('HTTP_USER_AGENT', ''),
                    is_active=True)
        except:
            device = None
        form = UserDeviceForm()
        return render(request, 'web/device.html',
                {'form': form, 'device': device})

@login_required
def dashboard(request):
    template = loader.get_template('web/dashboard.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
@ensure_csrf_cookie
def secrets(request):
    try:
        device = UserDevice.objects.get(user=request.user,
                agent=request.META.get('HTTP_USER_AGENT', ''),
                is_authorized=True,
                is_active=True)
    except:
        return redirect('device')
    secretvalues = SecretValue.objects.filter(userdevice=device)
    return render(request, 'web/secrets.html',
            {'secretvalues': secretvalues})

@login_required
def secret_create(request):
    try:
        device = UserDevice.objects.get(user=request.user,
                agent=request.META.get('HTTP_USER_AGENT', ''),
                is_authorized=True,
                is_active=True)
    except:
        return redirect('device')
    if request.method == 'POST':
        form = SecretForm(request.POST)
        if form.is_valid():
            return redirect('secrets')
    else:
        form = SecretForm()
    return render(request, 'web/secret_create.html',
            {'form': form, 'device': device})

@login_required
def secret_read(request, secret_id):
    try:
        device = UserDevice.objects.get(user=request.user,
                agent=request.META.get('HTTP_USER_AGENT', ''),
                is_authorized=True,
                is_active=True)
    except:
        return redirect('device')
    secret = get_object_or_404(Secret, pk=secret_id)
    secretvalue = SecretValue.objects.get(secret=secret,
                userdevice=device,
                is_active=True)
    return render(request, 'web/secret_read.html',
            {'secret': secret, 'device': device, 'secretvalue': secretvalue})

@login_required
def secret_update(request, secret_id):
    return render(request, 'web/secret_update.html')

@login_required
def secret_delete(request, secret_id):
    return render(request, 'web/secret_delete.html')
