from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Lesson, Attendance
from .forms import StudentForm, StudentModelForm



def index(request):
    return render(request, "attendance/index.html")

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "attendance/student_detail.html", {"student": student})

def student_list(request):
    students = Student.objects.all()
    return render(request, "attendance/student_list.html", {"students": students})

class HelloView(View):
    def get(self, request):
        return HttpResponse("Привет от CBV!")

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            return render(request, "attendance/success.html", {"student": form.cleaned_data})
    else:
        form = StudentForm()
    return render(request, "attendance/add_student.html", {"form": form})

def add_student_model(request):
    if request.method == "POST":
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentModelForm()
    return render(request, "attendance/add_student.html", {"form": form})



@login_required
def profile_dispatch(request):
    user = request.user
    # Фиксируем явный приоритет совмещённых ролей: преподаватель, затем студент
    if user.is_teacher:
        return redirect('teacher_cabinet')
    elif user.is_student:
        return redirect('student_cabinet')
    else:
        return redirect('general_profile')


@login_required
def student_cabinet(request):
    if not request.user.is_student:
        return render(request, 'attendance/no_access.html', {'role': 'Студент'})
    
    student = request.user.student
    attendances = Attendance.objects.filter(student=student)
    return render(request, 'attendance/student_cabinet.html', {
        'student': student,
        'attendances': attendances
    })


@login_required
def teacher_cabinet(request):
    if not request.user.is_teacher:
        return render(request, 'attendance/no_access.html', {'role': 'Преподаватель'})
    
    teacher = request.user.teacher
    lessons = Lesson.objects.filter(teacher=teacher)
    return render(request, 'attendance/teacher_cabinet.html', {
        'teacher': teacher,
        'lessons': lessons
    })


@login_required
def general_profile(request):
    return render(request, 'attendance/general_profile.html')