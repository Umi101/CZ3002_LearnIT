from django.contrib import admin

from .models import Course, Question, Reply

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Reply)
