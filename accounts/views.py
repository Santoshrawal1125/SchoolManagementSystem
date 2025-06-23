from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import CanCreateUsers


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "school": user.school_id,
            "department": user.department_id,
            "classroom": user.classroom_id,
        }

        if user.department:
            data["department_name"] = user.department.name

        if user.classroom:
            data["classroom_name"] = user.classroom.name

        return Response(data)


class RegisterView(APIView):
    permission_classes = [IsAuthenticated, CanCreateUsers, ]

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered"}, status=201)
        return Response(serializer.errors, status=400)
