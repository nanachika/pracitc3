import os
import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class User(AbstractUser):
    @property
    def is_student(self):
        return hasattr(self, 'student')
    
    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название группы")

    def __str__(self):
        return self.name

def avatar_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    uid = uuid.uuid4().hex
    today = datetime.now().strftime("%Y/%m/%d")
    return f"avatars/{today}/{uid}{ext}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")
    avatar = models.ImageField(upload_to=avatar_upload_to, default='avatars/default.jpg', verbose_name="Аватар")

    def __str__(self):
        p = self.patronymic[0] + "." if self.patronymic else ""
        return f"{self.last_name} {self.first_name[0]}. {p}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}. {self.patronymic[0] if self.patronymic else ''}."

class Lesson(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=50, verbose_name="Аудитория")

    def __str__(self):
        return f"{self.subject} ({self.date})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.student} {self.lesson}: {'V' if self.present else 'X'}"

def _delete_file(path):
    try:
        if path and os.path.isfile(path):
            os.remove(path)
    except Exception:
        pass

@receiver(post_delete, sender=Student)
def _student_avatar_delete_file(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.name != "avatars/default.jpg":
        _delete_file(instance.avatar.path)

@receiver(pre_save, sender=Student)
def _student_avatar_replace_file(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Student.objects.get(pk=instance.pk)
    except Student.DoesNotExist:
        return
    new_file = instance.avatar
    if old.avatar and old.avatar != new_file and old.avatar.name != "avatars/default.jpg":
        _delete_file(old.avatar.path)