from django.db import models
from django.contrib.auth.models import AbstractUser


# Кастомная модель пользователя с вычисляемыми свойствами ролей
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


# Профиль студента
class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student',
        verbose_name="Пользователь"
    )
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    group = models.CharField(max_length=20, verbose_name="Группа")

    def __str__(self):
        p = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.user.last_name} {self.user.first_name}{p} ({self.group})"


# Профиль преподавателя
class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher',
        verbose_name="Пользователь"
    )
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        p = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.user.last_name} {self.user.first_name}{p}".strip()


# Модель занятия
class Lesson(models.Model):
    date = models.DateField(verbose_name="Дата")
    subject = models.CharField(max_length=200, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    room = models.CharField(max_length=50, verbose_name="Аудитория")

    def __str__(self):
        return f"{self.subject} ({self.date})"


# Модель посещаемости
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Занятие")
    present = models.BooleanField(default=False, verbose_name="Присутствие")
    note = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.student} {self.lesson}: {'✓' if self.present else '❌'}"