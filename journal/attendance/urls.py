from django.urls import path
from . import views # импортируем функции из views.py
urlpatterns = [
    path('', views.index, name='attendance_index'),
    # http://127.0.0.1:8000/attendance/ - вызовет функцию index
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    #http://127.0.0.1:8000/attendance/student/1/ откроет страницу студента с id=1
    path('students/', views.student_list, name='student_list'),
    # http://127.0.0.1:8000/attendance/students/ + список всех студентов 
]