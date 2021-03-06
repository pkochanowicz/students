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

from students.views import SchoolView, SchoolClassView, StudentView, AddStudent,\
 StudentDeleteView, search_student

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', SchoolView.as_view(), name="index"),
    url(r'^class/(?P<school_class>(\d)+)$', SchoolClassView.as_view(), name="school_class"),
    url(r'^student/(?P<student_id>(\d+))$', StudentView.as_view(), name="student_view"),
    url(r'^add_student/', AddStudent.as_view(), name="add_student"),
    url(r'^delete_student/(?P<student_id>(\d+))$', StudentDeleteView.as_view(), name='warhammer-hero-delete'),
    url(r'^search_student/$', search_student, name="search_student"),

]
