from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Student, Shift

def check_assitance(req):
    if req.method == 'GET':
        return render(req, 'control/check.html')
    elif req.method == 'POST':
        pass


def view_progress(req):
    return render(req, 'control/progress.html')


def login_admin(req):
    if req.user.is_authenticated:
        return redirect('panel')

    if req.method == 'GET':
        return render(req, 'control/login.html')
    else:
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is None:
            return render(req, 'control/login.html', {'error': 'El usuario y la contraseña no coinciden'})
        else:
            login(req, user)
            return redirect('panel')

@login_required
def logout_admin(req):
    if req.method == 'POST':
        logout(req)
        return redirect('check')

@login_required(login_url='check')
def load_panel(req):
    return render(req, 'control/panel.html');

@login_required(login_url='check')
def edit_student(req):
    if req.method == 'GET':
        return render(req, 'control/edit.html')

    if req.method == 'POST':
        try:
            student = Student.objects.filter(id=req.POST.get("id"))[0]
            current_shifts = [shift.id for shift in student.shifts.all()]

        except:
            student = 'new'
            current_shifts = []

        shifts = Shift.objects.all()
        return render(req, 'control/edit.html', {"student": student, "shifts": shifts, "current_shifts": current_shifts})

@login_required(login_url='check')
def save_student_changes(req):
    if req.method == 'POST':
        id = req.POST.get('id')
        name = req.POST.get('name')
        email = req.POST.get('email')
        hours = req.POST.get('hours')
        shifts = req.POST.getlist('shifts[]')
        print(shifts)
        finger_print = req.POST.get('finger_print')

        try:
            student = Student.objects.filter(id=id)[0]
            student.shifts.clear()
            Student.objects.filter(id=id).update(name=name,
                                                 email=email,
                                                 hours_assigned=hours,
                                                 finger_print=finger_print)

        except:
            student = Student(  id = id,
                                name=name,
                                email=email,
                                hours_assigned=hours,
                                finger_print=finger_print)
            student.save()

        for shift in shifts:
            print(shift)
            student.shifts.add(Shift.objects.get(id=shift))

    return redirect('edit')
