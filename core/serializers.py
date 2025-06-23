from rest_framework import serializers
from .models import School, Department, Classroom


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['school'] = user.school
        return super().create(validated_data)


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['school'] = user.school
        return super().create(validated_data)
