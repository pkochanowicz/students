from django import forms

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, validate_email
from datetime import datetime

from .models import Student

class StudentSearchForm(forms.Form):
    name = forms.CharField(label="Search student", required=False)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'year_of_birth', 'school_class']
