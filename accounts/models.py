from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

ROLE_CHOICES = [
    ('superadmin', 'SuperAdmin'),
    ('schooladmin', 'SchoolAdmin'),
    ('departmenthead', 'DepartmentHead'),
    ('staff', 'Staff'),
    ('student', 'Student'),
]


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.ForeignKey('core.School', null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('core.Department', null=True, blank=True, on_delete=models.SET_NULL)
    classroom = models.ForeignKey('core.Classroom', null=True, blank=True, on_delete=models.SET_NULL)

    groups = models.ManyToManyField(
        Group,
        related_name='accounts_user_set',  # auth.User is a default name, so we should avoid that
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_user_set',  # auth.User is a default name, so we should avoid that
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Static role check helpers
    def is_superadmin(self):
        return self.role == 'superadmin'

    def is_schooladmin(self):
        return self.role == 'schooladmin'

    def is_department_head(self):
        return self.role == 'depthead'

    def is_classteacher(self):
        return self.role == 'classteacher'

    def is_student(self):
        return self.role == 'student'

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.role:
            self.role = 'superadmin'
        super().save(*args, **kwargs)
