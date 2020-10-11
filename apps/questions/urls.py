from django.urls import path

from .views.courses import CourseDetailView
from .views.questions import (IndexView, QuestionCreateView,
                              QuestionDeleteView, QuestionDetailView,
                              QuestionUpdateView, like_or_dislike_question,
                              mark_question_as_solved)
from .views.replies import (ReplyDeleteView, ReplyUpdateView,
                            like_or_dislike_reply)

urlpatterns = [
    path('search', IndexView.as_view(), name='search'),

    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course'),


    path('new', QuestionCreateView.as_view(), name='new_question'),
    path('<slug:slug>', QuestionDetailView.as_view(), name='question'),
    path('<slug:slug>/edit', QuestionUpdateView.as_view(), name='update_question'),
    path('<slug:slug>/delete', QuestionDeleteView.as_view(), name='delete_question'),
    path('<int:id>/solved', mark_question_as_solved, name='solve_question'),

    path('<slug:slug>/replies/<int:pk>/edit',
         ReplyUpdateView.as_view(), name='update_reply'),
    path('<slug:slug>/replies/<int:pk>/delete',
         ReplyDeleteView.as_view(), name='delete_reply'),

    path('questions/<int:id>/like-or-dislike',
         like_or_dislike_question, name='like_dislike'),
    path('replies/<int:id>/like-or-dislike',
         like_or_dislike_reply, name='like_dislike'),
]
