from django import forms
from .models import Student
from django.core.validators import FileExtensionValidator
from .models import Group

class StudentForm(forms.Form):
    last_name = forms.CharField(max_length=100, label="Фамилия")
    first_name = forms.CharField(max_length=100, label="Имя")
    patronymic = forms.CharField(max_length=100, required=False, label="Отчество")
    group = forms.CharField(max_length=20, label="Группа")

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'patronymic']

MAX_MB = 5

def validate_filesize(file):
    if file.size > MAX_MB * 1024 * 1024:
        raise forms.ValidationError(f"Размер файла не должен превышать {MAX_MB} МБ")

class StudentAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
            validate_filesize
        ],
        label="Аватар",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*", "class": "form-control"}),
        help_text="Загрузите изображение (JPEG/PNG), до 5 МБ"
    )

    class Meta:
        model = Student
        fields = ["avatar"]


class StudentFilterForm(forms.Form):
    last_name = forms.CharField(
        label="Часть фамилии",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Поиск по фамилии"})
    )
    group = forms.ModelChoiceField(
        label="Группа",
        queryset=Group.objects.all(),
        required=False,
        empty_label="Все группы",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    group_name = forms.CharField(
        label="Часть названия группы",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: ИВТ"})
    )