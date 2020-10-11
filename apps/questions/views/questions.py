from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic

from ..filters import questions_filter
from ..forms import ReplyForm
from ..models import Question, Reply


# class based views
class IndexView(generic.ListView):
    template_name = 'questions/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return questions_filter(self.request, Question)


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReplyForm

        return context

    def post(self, request, *args, **kwargs):
        form = ReplyForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.creator = request.user
            reply.question = self.get_object()
            reply.save()

            self.object = self.get_object()

            context = context = super().get_context_data(**kwargs)
            context['form'] = ReplyForm

            messages.success(
                self.request, 'Your reply is successfully submitted!')

            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)
            context['form'] = form

            return self.render_to_response(context=context)


class QuestionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Question
    fields = ['course', 'content', 'solved']
    template_name = 'questions/update_question.html'


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/accounts/login'
    model = Question
    template_name = 'questions/new_question.html'
    fields = ['course', 'title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(
            self.request, 'Your questions is successfully submitted!')
        return super().form_valid(form)


class QuestionDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Question
    success_url = reverse_lazy('index')


def like_or_dislike_question(request, id):
    try:
        question = Question.objects.get(pk=id)
        current_user = request.user

        if question.is_liked_by(current_user):
            question.dislike(current_user)
            return JsonResponse({'message': 'disliked'})

        question.like(current_user)
        return JsonResponse({'message': 'liked'})

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Question not found'})


def mark_question_as_solved(request, id):
    try:
        question = Question.objects.get(pk=id)
        question.solved = True
        question.save()

        return JsonResponse({'message': 'solved'})

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Question not found'})
