import copy
from django.db.models import Q
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from .models import Course, Selection

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()

        if not user:
            print("user not found")
            return render(request, 'user/login.html')
        if user.check_password(password):
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            print("password is wrong")
            return render(request, 'user/login.html')
    return render(request, 'user/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            new_user = User.objects.create_user(username=username, password=password, role='student')
            new_user.save()
            return redirect('login')
        except IntegrityError:
            print("The username is Repetitious")
            return redirect('register')
    return render(request, 'user/register.html')


def student_dashboard(request):
    if 'user_id' not in request.session or request.session['role'] != 'student':
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'user/student_dashboard.html', {'courses': courses})


def selected_courses(request):
    if 'user_id' not in request.session or request.session['role'] != 'student':
        return redirect('login')
    student_id = request.session['user_id']
    selections = Selection.objects.filter(student_id=student_id)
    return render(request, 'user/selected_courses.html', {'selections': selections})


def check_add_course_student(course: Course, student):
    schedule = course.schedule
    course_times = []
    times = schedule.split(' - ')
    for time in times:
        course_times.append(time.split(" "))

    selected_courses = Selection.objects.filter(student=student)
    for crs in selected_courses:
        times = crs.course.schedule.split(" - ")
        for time in times:
            day, turn = time.split(" ")
            for cheft in course_times:
                if day == cheft[0] and turn == cheft[1]:
                    return False
    return True


def select_course(request, course_id):
    user_id = request.session["user_id"]
    user = User.objects.get(pk=user_id)
    
    course = Course.objects.get(pk=course_id)
    
    if check_add_course_student(course=course, student=user):
        new_selection = Selection()
        new_selection.student = user
        new_selection.course = course
        new_selection.save()
        return render(request, 'user/selected_courses.html', {"selections": [new_selection]})

    else:
        print("Conflict in selecting")
        return render(request, 'user/conflict_select_course.html')

    

def remove_course(request, selection_id):
    selected = Selection.objects.get(pk=selection_id)
    b = copy.deepcopy(selected)
    selected.delete()
    return render(request, 'user/removed_course.html', {'course': b})


def search_courses(request):
    query = request.GET.get('search', '')
    result = Course.objects.filter(Q(course_name__contains=query) | Q(instructor_name__contains=query))
    return render(request, 'user/search_courses.html', {"courses": result})
