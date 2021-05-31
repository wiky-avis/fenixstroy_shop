from django.shortcuts import render, get_object_or_404
from .models import Gloves

from django.views.generic import DetailView


def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    model = Gloves
    queryset = Gloves.objects.all()
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
