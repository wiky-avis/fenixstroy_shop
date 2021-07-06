from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='blog'),
    path(
        '<slug:slug>/', views.ArticleDetailView.as_view(), name='blog_detail'),
]
