from django import forms
from testing.models import UserProfile,Posts
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('qualification', 'location')

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ('courseid',)