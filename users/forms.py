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
    preference_types = (
        ('A0101', '자연관광지'),
        ('A0102', '관광자원'),
        ('A0201', '역사관광지'),
        ('A0202', '휴양관광지'),
        ('A0203', '체험관광지'),
        ('A0204', '산업관광지'),
        ('A0205', '건축/조형물'),
        ('A0206', '문화시설'),
        ('A0207', '축제'),
        ('A0208', '공연/행사'),
    )
    preference = forms.MultipleChoiceField(choices = preference_types, label = "선호 유형")

    class Meta:
        model = Profile
        fields = ['image', 'disability', 'preference']