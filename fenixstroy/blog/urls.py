from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleView.as_view(), name='blog_all'),
    path(
        '<slug:slug>/',
        views.ArticleDetailView.as_view(),
        name='blog_detail'
        ),
    path('new_comment/', views.ArticleCommentCreateView.as_view(), name='new_comment'),
]
