from django.urls import path
from . import views

urlpatterns = [
    # Маршруты старые
    path('', views.index, name='attendance_index'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('students/', views.student_list, name='student_list'),
    path('student/add/', views.add_student, name='add_student'),
    path('student/add-model/', views.add_student_model, name='add_student_model'),

    # Маршруты новые
    path('profile/', views.profile_dispatch, name='profile_dispatch'),
    path('student-cabinet/', views.student_cabinet, name='student_cabinet'),
    path('teacher-cabinet/', views.teacher_cabinet, name='teacher_cabinet'),
    path('general-profile/', views.general_profile, name='general_profile'),
    path('upload-raw/', views.upload_raw, name='upload_raw'),
]