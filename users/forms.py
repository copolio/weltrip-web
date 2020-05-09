from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']    

class UserUpdateForm(forms.ModelForm): #inherit
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email'] # 지금은 username과 email만 수정 가능하도록 함

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'disability']