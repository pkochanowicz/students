"""trail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from students.views import SchoolView, SchoolClassView, StudentView, StudentGradesView, StudentSearch, \
     AddStudent, ListUsersView, UserLoginView, UserLogoutView, AddUserView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SchoolView.as_view(), name="index"),
    url(r'^class/(?P<school_class>(\d)+)$', SchoolClassView.as_view(), name="school_class"),
    url(r'^student/(?P<student_id>(\d+))$', StudentView.as_view(), name="student_view"),
    url(r'^grades/(?P<student_id>(\d+))(?P<subject_id>(\d+))$', StudentGradesView.as_view(), name="student_grades"),
    url(r'^student_search', StudentSearch.as_view(), name="student_search"),
    url(r'^add_student', AddStudent.as_view(), name="add_student"),


    url(r'^list_users', ListUsersView.as_view(), name='list_users'),
    url(r'^user_login', UserLoginView.as_view(), name='user_login'),
    url(r'^user_logout', UserLogoutView.as_view(), name='user_logout'),
    url(r'^add_user', AddUserView.as_view(), name='add_user'),
]
