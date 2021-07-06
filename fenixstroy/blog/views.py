from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.base import View

from .models import Article, ArticleComment, Category


class ArticleView(View):

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(published=True).all()
        return render(
            request, 'blog.html', {'articles': articles})


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog_details.html'
