from rest_framework import serializers
from .models import Staff, Student


class StaffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'name', 'department']


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'classroom']
