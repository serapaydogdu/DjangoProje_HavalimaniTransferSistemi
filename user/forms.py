from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username'    : TextInput(attrs={'class': 'input-group col-md-6','placeholder': 'username'}),
            'email'       : EmailInput(attrs={'class': 'input-group col-md-6','placeholder': 'email'}),
            'first_name'  : TextInput(attrs={'class': 'input-group col-md-6','placeholder': 'first_name'}),
            'last_name'   : TextInput(attrs={'class': 'input-group col-md-6','placeholder': 'last_name'}),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Karabuk', 'Karabuk'),
]

#Profile update form allows users to update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input-group col-md-6', 'placeholder': 'phone'}),
            'address'   : TextInput(attrs={'class': 'input-group col-md-6', 'placeholder': 'address'}),
            'city'      : Select(attrs={'class': 'input-group col-md-6', 'placeholder': 'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input-group col-md-6', 'placeholder': 'country'}),
            'image'     : FileInput(attrs={'class': 'input-group col-md-6', 'placeholder': 'image'}),
        }