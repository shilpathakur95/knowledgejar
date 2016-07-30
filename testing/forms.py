from django import forms
from testing.models import UserProfile,Posts,Course
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

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Posts
        exclude = ('courseid','created_on')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields=('course_name',)