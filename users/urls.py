from django.urls import path
from .views import StaffListView, StaffDetailView, DepartmentStaffListView, StudentListView, StudentDetailView, \
    ClassroomStudentListView

urlpatterns = [
    # staff endpoints
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('department/<int:pk>/staff/', DepartmentStaffListView.as_view(), name='department-staff-list'),

    # student endpoints
    path('students/', StudentListView.as_view(), name='student-list'),
    path('classroom/<int:pk>/students/', ClassroomStudentListView.as_view(), name='classroom-student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]
