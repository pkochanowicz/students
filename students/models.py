from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.
SCHOOL_CLASS = (
    (1, "1a"),
    (2, "1b"),
    (3, "2a"),
    (4, "2b"),
    (5, "3a"),
    (6, "3b"),
)

GRADES = (
    (1, "1"),
    (1.5, "1+"),
    (1.75, "2-"),
    (2, "2"),
    (2.5, "2+"),
    (2.75, "3-"),
    (3, "3"),
    (3.5, "3+"),
    (3.75, "4-"),
    (4, "4"),
    (4.5, "4+"),
    (4.75, "5-"),
    (5, "5"),
    (5.5, "5+"),
    (5.75, "6-"),
    (6, "6")
)

class SchoolSubject(models.Model):
    name = models.CharField(max_length=64)
    teacher_name = models.CharField(max_length=64)

    def __str__(self):
        return self.teacher_name


class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    school_class = models.IntegerField(choices=SCHOOL_CLASS)
    year_of_birth = models.IntegerField(validators=[MinValueValidator(1900),
                                                    MaxValueValidator(datetime.now().year)],
                                        blank=True,
                                        null=True)
    grades = models.ManyToManyField("SchoolSubject", through="StudentGrades")

    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name

class StudentGrades(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    school_subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES)
