from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth.decorators	import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q

from students.forms import StudentSearchForm, StudentForm
from students.models import SCHOOL_CLASS, Student
# Create your views here.

def search_student(request):
    form = StudentSearchForm(request.POST)
    clear = request.GET.get('clear', 'false')
    order_by = request.GET.get('order_by', 'last_name')
    ordering = order_by.lower()
    if clear == 'true':
        del request.session['searched_name']
    try:
        if form.is_valid() and (not request.session['searched_name']):
            searched_name = form.cleaned_data['name']
            request.session['searched_name'] = searched_name
            students = Student.objects.filter(Q(first_name__icontains=searched_name)\
                       |Q(last_name__icontains=searched_name)).order_by(ordering)
        if request.session['searched_name']:
            if (request.session['searched_name'] != form.cleaned_data['name']) & \
            (form.cleaned_data['name'] != ""):
                request.session['searched_name'] = form.cleaned_data['name']
            searched_name = request.session['searched_name']
            students = Student.objects.filter(Q(first_name__icontains=searched_name)\
                       |Q(last_name__icontains=searched_name)).order_by(ordering)
    except KeyError:
        students = Student.objects.all()
        request.session['searched_name'] = form.cleaned_data['name']

    paginator = Paginator(students, 4)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    return render(request, 'search.html',
                  {'form': form,
                  'students': students,
                   'order_by': order_by})

class SchoolView(View):

    def get(self, request):
        return render(request, 'class_list.html', {'school_classes': SCHOOL_CLASS})


class SchoolClassView(View):

    def get(self, request, school_class):
        students = Student.objects.filter(school_class=school_class).order_by('last_name')

        return render(request, "class.html", {"students": students,
                                              "class_name": SCHOOL_CLASS[int(school_class) - 1][1]})


class StudentView(View):

    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        return render(request, "student.html", {"student": student,
                                                "class_name": SCHOOL_CLASS[int(student.school_class) - 1][1]})

class AddStudent(View):

    def get(self, request):
        form = StudentForm()
        return render(request, 'add_student.html', {"form": form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            school_class = form.cleaned_data['school_class']
            year_of_birth = form.cleaned_data['year_of_birth']
            if Student.objects.filter(first_name=first_name, last_name=last_name).exists():
                message = "Student with that name is already registered."
                return render(request, 'add_student.html', {"form": form,
                                                            "message": message})
            new_student = Student.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            school_class=school_class,
                            year_of_birth=year_of_birth)
            return redirect("/student/{}".format(new_student.id))
        else:
            return render(request, 'add_student.html', {"form": form})

class StudentDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        student.delete()
        return redirect("/")
