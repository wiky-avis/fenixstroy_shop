from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.base import View

from .models import Article, ArticleComment, Category


class ArticleView(View):

    def get(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        articles = Article.objects.filter(published=True).all()
        return render(
            request, 'blog.html', {'articles': articles})


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog_details.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['articles'] = Article.objects.all()
        artticle = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        context['comments'] = artticle.article_comments.all()
        return context
