from django.db import models


class Shift(models.Model):
    week_day = models.CharField(max_length=10)
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return f"{self.week_day} ({self.start_hour}-{self.end_hour})"


class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    finger_print = models.CharField(max_length=100)
    hours_assigned = models.IntegerField(default=0)
    shifts = models.ManyToManyField(Shift)
