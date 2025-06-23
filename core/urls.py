from django.urls import path
from .views import SchoolListCreateView, SchoolDetailView, DepartmentListCreateView, DepartmentDetailView, \
    ClassroomListCreateView, ClassroomDetailView

urlpatterns = [

    # School endpoints
    path('schools/', SchoolListCreateView.as_view(), name='school-list-create'),
    path('school/<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),

    # Department endpoints
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('department/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),

    # Classroom endpoints
    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list-create'),
    path('classroom/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),

]
