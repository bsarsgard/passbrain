from django import forms

class UserDeviceForm(forms.Form):
    name = forms.CharField(label='Device Name', max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    public_key = forms.CharField(label='Public Key',
            widget=forms.Textarea(attrs={'class': 'form-control'}))

class SecretForm(forms.Form):
    label = forms.CharField(label='Label', max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.CharField(label='Value',
            widget=forms.Textarea(attrs={'class': 'form-control'}))
