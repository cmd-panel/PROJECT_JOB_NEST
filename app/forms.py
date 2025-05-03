from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, CV, Application, Course, CourseVideo

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    resume = forms.FileField(required=False)
    is_staff = forms.ChoiceField(
        choices=[('0', 'Regular User'), ('1', 'Employer')],
        widget=forms.RadioSelect,
        label="Register As"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password','is_staff']

def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])

    if commit:
        user.save()
        resume_file = self.cleaned_data.get('resume')
        # Create or get the profile instance
        profile, created = Profile.objects.get_or_create(user=user)
        if resume_file:
            profile.resume = resume_file
            profile.save()
    return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
    password = forms.CharField(widget=forms.PasswordInput)

class JobFilterForm(forms.Form):
    location = forms.CharField(required=False, label="Location")
    category = forms.CharField(required=False, label="Category")
    experience_level = forms.CharField(required=False, label="Experience Level")
    keyword = forms.CharField(required=False, label="Keyword")
#SUZANA   
from .models import Application

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
class ApplicationForm(forms.ModelForm):
     class Meta:
         model = Application
         fields = ['resume']
        
from .models import Portfolio

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Software Developer'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your job experience...'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://example.com/project'}),
        }



#wasib


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['name', 'email', 'phone', 'education', 'experience', 'skills']  


class ApplicationForm1(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['position', 'resume']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['title', 'youtube_url']

#end wasib

