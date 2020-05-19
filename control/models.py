from django.db import models

class Shift(models.Model):
    WEEK_DAYS = (
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo')
    )
    week_day = models.IntegerField(choices=WEEK_DAYS)
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return f"{self.get_week_day_display()} ({self.start_hour}-{self.end_hour})"

class TimeSheet(models.Model):
    name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.name} timesheet"

class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    finger_print = models.CharField(max_length=100)
    hours_assigned = models.IntegerField(default=0)
    shifts = models.ManyToManyField(Shift)
    time_sheet = models.ForeignKey(TimeSheet, on_delete=models.CASCADE, null=True)

class AssistanceLog(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    time_sheet = models.ForeignKey(TimeSheet, on_delete=models.CASCADE)
