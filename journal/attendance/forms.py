from django import forms
from .models import Student

class StudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, label="Фамилия")
    first_name = forms.CharField(max_length=100, label="Имя")
    patronymic = forms.CharField(max_length=100, required=False, label="Отчество")
    group = forms.CharField(max_length=20, label="Группа")

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'patronymic']