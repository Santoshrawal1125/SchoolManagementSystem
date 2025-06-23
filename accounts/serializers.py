from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, serializers
from users.models import Staff, Student
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom data for more clarity while logging in.
        token['role'] = user.role
        token['username'] = user.username
        token['school_id'] = user.school_id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['school_id'] = self.user.school_id
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'school', 'department', 'classroom']

    def validate(self, attrs):
        creator = self.context['request'].user
        role = attrs.get('role')
        school = attrs.get('school')
        department = attrs.get('department')
        classroom = attrs.get('classroom')

        # SuperAdmin creates SchoolAdmin
        if creator.role == 'superadmin':
            if role != 'schooladmin':
                raise serializers.ValidationError("SuperAdmin can only create SchoolAdmins.")
            if not school:
                raise serializers.ValidationError("You must assign a school to the SchoolAdmin.")
            if User.objects.filter(role='schooladmin', school=school).exists():
                raise serializers.ValidationError("This school already has a SchoolAdmin.")

        # SchoolAdmin creates depthead, staff, or student
        elif creator.role == 'schooladmin':
            # School spoofing prevention
            if school and school != creator.school:
                raise serializers.ValidationError("You can only assign users to your own school.")
            attrs['school'] = creator.school

            if role == 'departmenthead':
                if not department:
                    raise serializers.ValidationError({"department": "Department is required for DepartmentHead."})
                if department.school != creator.school:
                    raise serializers.ValidationError("You cannot assign a department from another school.")
                if classroom:
                    raise serializers.ValidationError({"classroom": "DepartmentHead should not have a classroom."})

            elif role == 'staff':
                if not department:
                    raise serializers.ValidationError({"department": "Department is required for Staff."})
                if department.school != creator.school:
                    raise serializers.ValidationError("You cannot assign a department from another school.")
                if classroom:
                    raise serializers.ValidationError({"classroom": "Staff should not have a classroom."})

            elif role == 'student':
                if not classroom:
                    raise serializers.ValidationError({"classroom": "Classroom is required for Student."})
                if classroom.school != creator.school:
                    raise serializers.ValidationError("You cannot assign a classroom from another school.")
                if department:
                    raise serializers.ValidationError({"department": "Student should not have a department."})

            else:
                raise serializers.ValidationError("SchoolAdmin can only create Staff, Student, or DepartmentHead.")

        else:
            raise serializers.ValidationError("You are not allowed to create users.")

        return attrs

    def create(self, validated_data):
        role = validated_data['role']
        department = validated_data.get('department')
        classroom = validated_data.get('classroom')
        school = validated_data.get('school')

        # Create main User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role,
            school=school,
            department=department,
            classroom=classroom,
        )

        # 🔁 Create related models
        if role == 'staff':
            Staff.objects.create(
                user=user,
                department=department,
                designation=""
            )

        elif role == 'student':
            Student.objects.create(
                user=user,
                roll_number=user.username,
                classroom=classroom,
                guardian_name=""
            )

        return user
