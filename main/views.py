from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Course, Selection

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
    return render(request, 'main/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        new_user = User.objects.create_user(username=username, password=password, role='student')
        new_user.save()
        return redirect('login')
    return render(request, 'main/register.html')

def admin_dashboard(request):
    if 'user_id' not in request.session or request.session['role'] != 'admin':
        return redirect('login')
    if request.method == 'POST':
        course_name = request.POST['course_name']
        instructor_name = request.POST['instructor_name']
        schedule = request.POST['schedule']
        new_course = Course(course_name=course_name, instructor_name=instructor_name, schedule=schedule)
        new_course.save()
    courses = Course.objects.all()
    return render(request, 'main/admin_dashboard.html', {'courses': courses})

def student_dashboard(request):
    if 'user_id' not in request.session or request.session['role'] != 'student':
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'main/student_dashboard.html', {'courses': courses})

def selected_courses(request):
    if 'user_id' not in request.session or request.session['role'] != 'student':
        return redirect('login')
    student_id = request.session['user_id']
    selections = Selection.objects.filter(student_id=student_id)
    return render(request, 'main/selected_courses.html', {'selections': selections})