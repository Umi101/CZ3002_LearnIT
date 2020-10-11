from django.http import Http404, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from ..models import Question, Reply


class ReplyUpdateView(generic.UpdateView):
    model = Reply
    fields = ['content', ]
    template_name = 'questions/update_reply.html'

    def get_object(self, queryset=None):
        obj = super().get_object()

        if not obj.creator == self.request.user:
            raise Http404

        question = Question.objects.get(slug=obj.question.slug)
        self.question = question

        return obj

    def get_success_url(self):
        return reverse_lazy('question', args=(self.question.slug,))


class ReplyDeleteView(generic.edit.DeleteView):
    model = Reply

    def get_object(self, queryset=None):
        obj = super().get_object()

        if not obj.creator == self.request.user:
            raise Http404

        question = Question.objects.get(slug=obj.question.slug)
        self.question = question

        return obj

    def get_success_url(self):
        return reverse_lazy('question', args=(self.question.slug,))


def like_or_dislike_reply(request, id):
    reply = get_object_or_404(Reply, pk=id)
    current_user = request.user

    if reply.is_liked_by(current_user):
        reply.dislike(current_user)
        return JsonResponse({'message': 'disliked'})

    reply.like(current_user)
    return JsonResponse({'message': 'liked'})
