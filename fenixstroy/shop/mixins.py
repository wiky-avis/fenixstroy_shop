from django.views.generic.detail import SingleObjectMixin

from .models import Category
from django.views.generic.base import View
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(published=True).all()
        return context
