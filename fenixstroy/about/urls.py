from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
