from django.db import models
from accounts.models import User
from core.models import Department, Classroom


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100, blank=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"
