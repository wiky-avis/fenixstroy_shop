from django.shortcuts import render, get_object_or_404
from .models import Gloves, Comment, Product
from django.db.models import Avg

from django.views.generic import DetailView


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    model = Gloves
    queryset = Gloves.objects.filter(published=True).all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        gloves = get_object_or_404(Gloves, slug=self.kwargs['slug'])
        int_rating = gloves.comments.all().aggregate(Avg('score'))
        context['int_rating'] = int_rating['score__avg']
        if context['int_rating'] is None:
            context['int_rating'] = 0
        return context
