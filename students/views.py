from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth.decorators	import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from students.forms import StudentSearchForm, AddStudentForm, UserForm, StudentForm, UserLoginForm, AddUserForm
from students.models import SCHOOL_CLASS, Student, SchoolSubject, StudentGrades
# Create your views here.
class SchoolView(View):

    def get(self, request):
        return render(request, 'class_list.html', {'school_classes': SCHOOL_CLASS})


class SchoolClassView(View):

    def get(self, request, school_class):
        students_list = Student.objects.filter(school_class=school_class).order_by('last_name')
        paginator = Paginator(students_list, 5)

        page = request.GET.get('page')
        students = paginator.get_page(page)

        return render(request, "class.html", {"students": students,
                                              "class_name": SCHOOL_CLASS[int(school_class) - 1][1]})


class StudentView(View):

    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        return render(request, "student.html", {"student": student,
                                                "class_name": SCHOOL_CLASS[int(student.school_class) - 1][1]})


class StudentGradesView(View):

    def get(self, request, student_id, subject_id):
        student = Student.objects.get(id=student_id)
        subject = SchoolSubject.objects.get(id=subject_id)
        grades = StudentGrades.objects.filter(student=student_id)
        grades = grades.filter(school_subject=subject_id)
        grade_average = grades.aggregate(Avg('grade'))
        return render(request, "student_grades.html", {"student": student,
                                                       "subject": subject,
                                                       "grades": grades,
                                                       "class_name": SCHOOL_CLASS[int(student.school_class) - 1][1],
                                                       "grade_average": grade_average['grade__avg']})


class StudentSearch(View):

    def get(self, request):
        form = StudentSearchForm()
        return render(request, 'search.html', {'form': form})

    def post(self, request):
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            students = Student.objects.filter(last_name__icontains=last_name)
            return render(request, 'students.html', {'students': students})


class AddStudent(View):

    def get(self, request):
        form = AddStudentForm()
        return render(request, 'add_student.html', {"form": form})

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            student_class = form.cleaned_data['student_class']
            year_of_birth = form.cleaned_data['year_of_birth']
            new_student = Student.objects.create(
                            first_name=first_name,
                            last_name=last_name,
                            school_class=student_class,
                            year_of_birth=year_of_birth)
            return redirect("/student/{}".format(new_student.id), code=402)
        else:
            return render(request, 'add_student.html', {"form": form})

class ListUsersView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'list_users.html', {'users': users})


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'user_login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list_users')
            else:
                return render(request, 'user_login.html', {'form': form,
                                                           'message': 'Wrong login or password'})


class UserLogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('/user_login')


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeated_password = form.cleaned_data['repeat_password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            if password != repeated_password:
                return render(request, 'add_user.html', {'form': form,
                                                         'message': 'Passwords don\'t match'})
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return render(request, 'add_user.html', {'form': form,
                                                         'message': 'User with that name or email already exists.'})
            User.objects.create_user(username=username, email=email, password=password,
                                     first_name=first_name, last_name=last_name)
            return render(request, 'add_user.html', {'form': form,
                                                     'message': 'User created'})
        else:
            return render(request, 'add_user.html', {'form': form,
                                                     'message': 'Form is invalid.'})
