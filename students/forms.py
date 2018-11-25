from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, validate_email

from .models import Student


class StudentSearchForm(forms.Form):
    last_name = forms.CharField(label="search by last name ", required=False)


class AddStudentForm(forms.Form):
    first_name = forms.CharField(label="Student's first name", required=False, max_length=64, strip=True)
    last_name = forms.CharField(label="Student's last name", required=False, max_length=64, strip=True)
    year_of_birth = forms.IntegerField(label="Student's year of birth", required=False)
    student_class = forms.ChoiceField(choices=(("1", "1a"),
                                               ("2", "1b"),
                                               ("3", "2a"),
                                               ("4", "2b"),
                                               ("5", "3a"),
                                               ("6", "3b"),))


class UserForm(forms.Form):
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    email = forms.CharField(label='email', validators=[EmailValidator(message='zly email')])
    url = forms.CharField(validators=[URLValidator(message='zly url')])


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'school_class', 'year_of_birth']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='user_name')
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    username = forms.CharField(label='User name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)
    email = forms.CharField(label='E-mail', validators=[validate_email])
