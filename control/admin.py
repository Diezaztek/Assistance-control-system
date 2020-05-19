from django.contrib import admin
from .models import Student, Shift, TimeSheet, AssistanceLog

admin.site.register(Student)
admin.site.register(Shift)
admin.site.register(TimeSheet)
admin.site.register(AssistanceLog)
