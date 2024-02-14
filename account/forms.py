from django import forms
from django.contrib.auth.models import User
from courses.models import Course


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not macth themselves')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already registered')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=data).exists():
            raise forms.ValidationError('Email already registered')
        return data


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)
