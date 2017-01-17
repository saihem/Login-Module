from django import forms

from login.models import UserProfile
# from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", min_length=8, required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

    class Meta:
        model = UserProfile
        fields = ('name', 'username', 'password')
