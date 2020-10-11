from django import forms

from .models import Reply


class ReplyForm(forms.ModelForm):

    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Leave your reply...',
            'rows': 4,
        })
    )

    class Meta:
        model = Reply
        fields = ('content',)
