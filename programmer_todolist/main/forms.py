from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProgrammerProfile, Project, ProjectSubmission


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            ProgrammerProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data.get('phone', ''),
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProgrammerProfile
        fields = ['full_name', 'email', 'phone', 'skills', 'profile_picture']
        widgets = {
            'skills': forms.CheckboxSelectMultiple(
                choices=ProgrammerProfile.SKILL_CHOICES
            ),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'requirements', 'priority', 'deadline', 'assigned_to']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
        }


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = ProjectSubmission
        fields = ['submitted_file', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
