from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('selected_courses/', views.selected_courses, name='selected_courses'),
    path('select_courses/<course_id>', views.select_course, name='select_course'),
    path('removed_course/<selection_id>', views.remove_course, name='remove_course'),
]
