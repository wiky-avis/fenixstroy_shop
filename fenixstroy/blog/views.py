from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from .models import Article, ArticleComment, Category
from .forms import ArticleCommentForm


class ArticleView(View):

    def get(self, request, *args, **kwargs):
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
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        context['comments'] = article.article_comments.all()
        context['form'] = ArticleCommentForm()
        return context


class ArticleCommentCreateView(CreateView):
    model = ArticleComment
    template_name = 'blog_details.html'
    fields = ['author', 'text']

    def form_valid(self, form):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        return redirect(
            'blog:blog_detail', slug=article.slug)

    def get_context_data(self, **kwargs):
        context = super(
            ArticleCommentCreateView, self
            ).get_context_data(**kwargs)
        context['article'] = get_object_or_404(
            Article, slug=self.kwargs.get('slug')
            )
        return context
