from django import forms
class StudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, label="Фамилия")
    first_name = forms.CharField(max_length=100, label="Имя")
    group = forms.CharField(max_length=20, label="Группа")

from .models import Student
class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group']