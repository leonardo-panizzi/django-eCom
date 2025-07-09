# cart/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm

from store.forms import UpdateUserForm


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'placeholder': 'New Password'}),
            'new_password2': forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        }
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Avoid a password that is too similar to your other personal information.</li><li>Your password must contain at least 8 characters and it can\'t be entirely numeric.</li></ul>'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Confirm your password by re-typing it.</small></span>'


class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
    }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
            field.widget.attrs['class'] = 'form-control'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']