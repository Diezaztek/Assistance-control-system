import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student, Shift, TimeSheet, AssistanceLog

def check_assitance(req):
    if req.user.is_authenticated:
        return redirect('admin_check')

    if req.method == 'GET':
        return render(req, 'control/check.html')
    elif req.method == 'POST':
        pass


def view_progress(req, id):
    student = Student.objects.filter(id=id)[0]
    time_sheet = student.time_sheet
    assistance_logs = AssistanceLog.objects.filter(time_sheet=time_sheet)

    total_hours = 0
    for hours in assistance_logs:
        if hours.end_date:
            total_hours += ( ( hours.end_date.hour*60 ) + hours.end_date.minute ) - ( ( hours.start_date.hour*60 ) + hours.start_date.minute )


    return render(req, 'control/progress.html', {'assistance_logs': assistance_logs,
                                                'hours_worked': total_hours/60,
                                                'hours_assigned': student.hours_assigned,
                                                'completion': ((total_hours/60) / student.hours_assigned) * 100})


def login_admin(req):
    if req.user.is_authenticated:
        return redirect('admin_check')

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
            return redirect('admin_check')

@login_required
def logout_admin(req):
    if req.method == 'POST':
        logout(req)
        return redirect('check')

@login_required(login_url='check')
def admin_check(req):
    if req.method == 'GET':
        return render(req, 'control/panel.html');


@login_required(login_url='check')
def admin_check_in(req):
    if req.method == 'POST':

        now = datetime.datetime.now()
        try:
            student = Student.objects.get(id=req.POST.get('id'))
            time_sheet = student.time_sheet

            if AssistanceLog.objects.filter(time_sheet=time_sheet, end_date__isnull=True):
                messages.error(req, 'El estudiante ya checó su entrada')
                return redirect('admin_check')

            shifts = [(shift.week_day, shift.start_hour, shift.end_hour) for shift in student.shifts.all()]
            is_in_schedule = False
        except:
            messages.error(req, 'El estudiante no está dado de alta en la aplicación')
            return redirect('admin_check')

        for shift in shifts:
            if now.weekday() != shift[0]:
                continue
            else:
                start_time = int(shift[1].hour * 60) + int(shift[1].minute)
                end_time = int(shift[2].hour * 60) + int(shift[2].minute)
                current_time = int(now.hour * 60) + int(now.minute)
                if start_time <= current_time and end_time >= current_time:
                    is_in_schedule = True
                else:
                    continue

        if is_in_schedule:
            time_sheet = student.time_sheet
            assistance = AssistanceLog(start_date=now, time_sheet=time_sheet)
            assistance.save()
            messages.success(req, 'Cambios guardados correctamente')
            return redirect('admin_check')
        else:
            messages.error(req, 'El estudiante no puede hacer servicio becario en este horario')
            return redirect('admin_check')

@login_required(login_url='check')
def admin_check_out(req):
    if req.method == 'POST':
        now = datetime.datetime.now()
        student = Student.objects.get(id=req.POST.get('id'))
        time_sheet = student.time_sheet

        try:
            student = Student.objects.get(id=req.POST.get('id'))
            time_sheet = student.time_sheet

            if not (AssistanceLog.objects.filter(time_sheet=time_sheet, end_date__isnull=True)):
                messages.error(req, 'El estudiante no ha checado una entrada')
                return redirect('admin_check')

            AssistanceLog.objects.filter(time_sheet=time_sheet, end_date__isnull=True).update(end_date=now)
            messages.success(req, 'Se ha registrado exitosamente la salida')
            return redirect('admin_check')

        except:
            messages.error(req, 'El estudiante no está dado de alta en la aplicación')
            return redirect('admin_check')





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
        finger_print = req.POST.get('finger_print')

        try:
            student = Student.objects.filter(id=id)[0]
            student.shifts.clear()
            Student.objects.filter(id=id).update(name=name,
                                                 email=email,
                                                 hours_assigned=hours,
                                                 finger_print=finger_print)

        except:
            time_sheet = TimeSheet(name=id)
            time_sheet.save()

            student = Student(  id = id,
                                name=name,
                                email=email,
                                hours_assigned=hours,
                                finger_print=finger_print,
                                time_sheet = time_sheet)
            student.save()

        for shift in shifts:
            student.shifts.add(Shift.objects.get(id=shift))

        messages.add_message(req, messages.SUCCESS, 'Cambios guardados correctamente')

    return redirect('edit')

@login_required(login_url='check')
def view_summary(req):
    if req.method == 'GET':
        all_data = list()
        students = Student.objects.all().order_by('id')

        for student in students:
            time_sheet = student.time_sheet
            hours_log = AssistanceLog.objects.filter(time_sheet=time_sheet)

            total_hours = 0
            for hours in hours_log:
                if hours.end_date:
                    total_hours += ( ( hours.end_date.hour*60 ) + hours.end_date.minute ) - ( ( hours.start_date.hour*60 ) + hours.start_date.minute )

            all_data.append({
                'id': student.id,
                'name': student.name,
                'hours_assigned': student.hours_assigned,
                'hours_worked': total_hours/60
            })
        return render(req, 'control/summary.html', {'students': all_data})

    if req.method == 'POST':
        all_data = list()
        students = Student.objects.filter(id=req.POST.get('id')).order_by('id')

        for student in students:
            time_sheet = student.time_sheet
            hours_log = AssistanceLog.objects.filter(time_sheet=time_sheet)

            total_hours = 0
            for hours in hours_log:
                if hours.end_date:
                    total_hours += ( ( hours.end_date.hour*60 ) + hours.end_date.minute ) - ( ( hours.start_date.hour*60 ) + hours.start_date.minute )

            all_data.append({
                'id': student.id,
                'name': student.name,
                'hours_assigned': student.hours_assigned,
                'hours_worked': total_hours/60
            })
        return render(req, 'control/summary.html', {'students': all_data})
