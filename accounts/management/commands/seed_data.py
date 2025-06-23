from django.core.management.base import BaseCommand
from accounts.models import User
from core.models import School, Department, Classroom
from users.models import Staff, Student


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        # Create SuperAdmin
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser(username='superadmin', password='admin123', role='superadmin')
            self.stdout.write(self.style.SUCCESS("✅ SuperAdmin created"))

        for i in range(1, 3):
            # Create School
            school = School.objects.create(name=f"School {i}")
            self.stdout.write(self.style.SUCCESS(f"🏫 Created School {i}"))

            # Create SchoolAdmin
            school_admin = User.objects.create_user(
                username=f"schooladmin{i}",
                password="admin123",
                role="schooladmin",
                school=school
            )
            self.stdout.write(self.style.SUCCESS(f"👨‍💼 Created SchoolAdmin {i}"))

            # Create Departments
            dept1 = Department.objects.create(name=f"Math{i}", school=school)
            dept2 = Department.objects.create(name=f"Science{i}", school=school)

            # Create Classrooms
            class1 = Classroom.objects.create(name=f"ClassA{i}", school=school)
            class2 = Classroom.objects.create(name=f"ClassB{i}", school=school)

            self.stdout.write(self.style.SUCCESS(f"🏫 Created 2 Departments and 2 Classrooms for School {i}"))

            # Create Department Heads
            dh1 = User.objects.create_user(
                username=f"mathhead{i}",
                password="admin123",
                role="departmenthead",
                school=school,
                department=dept1
            )
            dh2 = User.objects.create_user(
                username=f"sciencehead{i}",
                password="admin123",
                role="departmenthead",
                school=school,
                department=dept2
            )
            self.stdout.write(self.style.SUCCESS(f"👨‍🏫 Created 2 DepartmentHeads for School {i}"))

            # Create Staff
            staff1_user = User.objects.create_user(
                username=f"staff{i}a",
                password="admin123",
                role="staff",
                school=school,
                department=dept1
            )
            Staff.objects.create(user=staff1_user, designation="Math Teacher", department=dept1)

            staff2_user = User.objects.create_user(
                username=f"staff{i}b",
                password="admin123",
                role="staff",
                school=school,
                department=dept2
            )
            Staff.objects.create(user=staff2_user, designation="Science Teacher", department=dept2)

            self.stdout.write(self.style.SUCCESS(f"👨‍🏫 Created 2 Staff for School {i}"))

            # Create Students
            student1_user = User.objects.create_user(
                username=f"student{i}a",
                password="admin123",
                role="student",
                school=school,
                classroom=class1
            )
            Student.objects.create(user=student1_user, roll_number=f"{i}01", guardian_name="Parent A", classroom=class1)

            student2_user = User.objects.create_user(
                username=f"student{i}b",
                password="admin123",
                role="student",
                school=school,
                classroom=class2
            )
            Student.objects.create(user=student2_user, roll_number=f"{i}02", guardian_name="Parent B", classroom=class2)

            self.stdout.write(self.style.SUCCESS(f"🎓 Created 2 Students for School {i}"))

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
