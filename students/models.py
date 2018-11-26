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

class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    school_class = models.IntegerField(choices=SCHOOL_CLASS)
    year_of_birth = models.IntegerField(validators=[MinValueValidator(1900),
                                                    MaxValueValidator(datetime.now().year - 4)],
                                        blank=True,
                                        null=True)

    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name
