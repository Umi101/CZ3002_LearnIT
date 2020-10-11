from django.views import generic

from ..models import Course


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'questions/course.html'
