from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    quality_score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'Stars'}))
    price_score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'Stars'}))

    class Meta:
        model = Comment
        fields = ['quality_score', 'price_score', 'author', 'text']
        # widgets = {
        #     'quality_score': forms.NumberInput(attrs={'class': 'Comment'}),
        #     'price_score': forms.NumberInput(attrs={'class': 'Comment'})
        #     }
