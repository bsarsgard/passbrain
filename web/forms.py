from django import forms
from django.contrib.auth.models import User

from secrets.models import SecretGroup, Trust, TrustUser


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
    groups = forms.ModelMultipleChoiceField(label='Groups',
            widget=forms.CheckboxSelectMultiple,
            queryset=SecretGroup.objects.all())

    def __init__(self, user, *args, **kwargs):
        super(SecretForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['groups'].queryset = SecretGroup.objects.filter(
                    users=user, is_hidden=False, is_active=True)
            self.initial['groups'] = SecretGroup.objects.filter(users=user,
                    is_default=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SecretGroupForm(forms.ModelForm):
    class Meta:
        model = SecretGroup
        fields = ['label', 'users']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'users': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, trust, *args, **kwargs):
        super(SecretGroupForm, self).__init__(*args, **kwargs)
        if trust:
            self.fields['users'].queryset = trust.users


class TrustForm(forms.ModelForm):
    class Meta:
        model = Trust
        fields = ['label']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TrustUserCreateForm(forms.Form):
    email = forms.CharField(label='Email addresses (one per line)',
            widget=forms.Textarea(attrs={'class': 'form-control'}))

    def process(self, trust):
        emails = self.cleaned_data['email']
        for email in emails.split('\n'):
            try:
                user = User.objects.get(email=email)
                trustuser = TrustUser(user=user, trust=trust)
                trustuser.save()
            except:
                pass
