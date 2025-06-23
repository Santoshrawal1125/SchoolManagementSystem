from django.shortcuts import render
from rest_framework import status

from .serializers import SchoolSerializer, DepartmentSerializer, ClassroomSerializer
from rest_framework.views import APIView
from .models import School, Classroom, Department
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSuperAdmin, CanCreateDepartmentAndClasses, CanAccessOwnSchoolOnly


class SchoolListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolDetailView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request, pk):
        school = get_object_or_404(School, pk=pk)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)

    def put(self, request, pk):
        school = get_object_or_404(School, pk=pk)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        school = get_object_or_404(School, pk=pk)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 🔹 Department Views
class DepartmentListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanAccessOwnSchoolOnly, CanCreateDepartmentAndClasses]

    def get(self, request):
        user = request.user
        if user.role == "schooladmin":
            departments = Department.objects.filter(school=user.school)
        else:
            departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            department = serializer.save()
            self.check_object_permissions(request, department)  # 🔐 object-level check after creation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated, CanAccessOwnSchoolOnly, CanCreateDepartmentAndClasses]

    def get_object(self, pk):
        obj = get_object_or_404(Department, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 🔹 Classroom Views
class ClassroomListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanAccessOwnSchoolOnly, CanCreateDepartmentAndClasses]

    def get(self, request):
        user = request.user
        if user.role == "schooladmin":
            classrooms = Classroom.objects.filter(school=user.school)
        else:
            classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassroomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            classroom = serializer.save()
            self.check_object_permissions(request, classroom)  # 🔐
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomDetailView(APIView):
    permission_classes = [IsAuthenticated, CanAccessOwnSchoolOnly, CanCreateDepartmentAndClasses]

    def get_object(self, pk):
        obj = get_object_or_404(Classroom, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom)
        return Response(serializer.data)

    def put(self, request, pk):
        classroom = self.get_object(pk)
        serializer = ClassroomSerializer(classroom, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        classroom = self.get_object(pk)
        classroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
