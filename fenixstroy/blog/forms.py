from django import forms

from .models import ArticleComment


class ArticleCommentForm(forms.ModelForm):

    class Meta:
        model = ArticleComment
        fields = ['author', 'text']
