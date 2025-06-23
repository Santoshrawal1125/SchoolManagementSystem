from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import StaffSerializer, StudentSerializer
from .models import Student, Staff
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import CanCreateDepartmentAndClasses, IsDepartmentHeadAndOwnDepartment


class StaffListView(ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'schooladmin':
            return Staff.objects.filter(department__school=user.school)

        elif user.role == 'departmenthead':
            return Staff.objects.filter(department=user.department)

        return Staff.objects.none()


class DepartmentStaffListView(ListAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        dept_id = self.kwargs.get('pk')

        queryset = Staff.objects.filter(department__id=dept_id)

        if user.role == 'schooladmin':
            return queryset.filter(department__school=user.school)

        elif user.role == 'depthead':
            return queryset.filter(department=user.department, department__id=dept_id)

        return Staff.objects.none()


class StaffDetailView(RetrieveAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsDepartmentHeadAndOwnDepartment]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'schooladmin':
            return Staff.objects.filter(department__school=user.school)

        elif user.role == 'depthead':
            return Staff.objects.filter(department=user.department)

        return Staff.objects.none()


class StudentListView(ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'schooladmin':
            return Student.objects.filter(classroom__school=user.school)

        return Student.objects.none()


class ClassroomStudentListView(ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        class_id = self.kwargs.get('pk')

        queryset = Student.objects.filter(classroom__id=class_id)

        if user.role == 'schooladmin':
            return queryset.filter(classroom__school=user.school)

        return Student.objects.none()


class StudentDetailView(RetrieveAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'schooladmin':
            return Student.objects.filter(classroom__school=user.school)

        return Student.objects.none()
