from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, related_name='departments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, related_name='classrooms', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.school.name})"
