from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Course, Selection
from django.contrib.auth import get_user_model



User = get_user_model()
try:
    admin_manager = User.objects.create_user(username="admin", password="admin123", role="admin")
    admin_manager.save()
except Exception as e:
    pass


def check_addable_course(course_name, proff_name, schedule):
    courses: list[Course] = Course.objects.all()
    for course in courses:
        if course_name == course.course_name:
            if proff_name == course.instructor_name:
                return False
    return True


def admin_dashboard(request):
    if 'user_id' not in request.session or request.session['role'] != 'admin':
        return redirect('login')
    if request.method == 'POST':
        course_name = request.POST['course_name']
        instructor_name = request.POST['instructor_name']
        schedule = request.POST['schedule']
        if check_addable_course(course_name, instructor_name, schedule):
            new_course = Course(course_name=course_name, instructor_name=instructor_name, schedule=schedule)
            new_course.save()
    courses = Course.objects.all()
    return render(request, 'user/admin_dashboard.html', {'courses': courses})


