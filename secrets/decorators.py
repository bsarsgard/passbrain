from django.shortcuts import redirect

from .models import UserDevice

def device_required(function=None):
    """
    Make sure the user has an authorized device
    """
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            try:
                device = UserDevice.objects.get(user=request.user,
                        id=request.COOKIES.get('userdevice_id', 0),
                        is_authorized=True,
                        is_active=True)
            except:
                device = None
            if device:
                device.agent = request.META.get('HTTP_USER_AGENT', '')
                device.ip_address = request.META.get('REMOTE_ADDR', '')
                device.save()
                kwargs['device'] = device
                return view_func(request, *args, **kwargs)
            else:
                return redirect('device')

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
