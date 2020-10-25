from django.contrib import admin

from .models import Course, Question, Reply, ReportedQuestion, ReportedReply

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(ReportedQuestion)
admin.site.register(ReportedReply)
