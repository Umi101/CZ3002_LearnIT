from hashlib import md5

from django import template
from django.contrib.auth.models import User

from apps.questions.models import Course, Question, Reply

register = template.Library()


@register.inclusion_tag('questions/_courses.html')
def show_courses():
    courses = Course.objects.all()
    return {'courses': courses}


@register.simple_tag
def reply_liked_by(reply, user):
    return reply.is_liked_by(user)


@register.simple_tag
def question_liked_by(question, user):
    return question.is_liked_by(user)


@register.filter(name='gravatar')
def gravatar(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = "//www.gravatar.com/avatar/{0}?s={1}&d=identicon&r=PG"
    return url.format(email_hash, size)
