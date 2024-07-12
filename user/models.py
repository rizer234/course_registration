from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=10)
        

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    instructor_name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=50)

class Selection(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
