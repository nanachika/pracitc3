from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from .models import Student
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