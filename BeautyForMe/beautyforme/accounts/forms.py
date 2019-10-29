from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "last_name", "email")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        if commit:
            user.save()
            user_profile = Profile.objects.get(user=user)
            user_profile.email = user.email
            user_profile.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("email", "nickname", "phone", "zip_code", "address", "address_detail")