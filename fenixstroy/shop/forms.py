from django import forms

from .models import Comment, RatingStar


class CommentForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Comment
        fields = ['star', 'author', 'text']
