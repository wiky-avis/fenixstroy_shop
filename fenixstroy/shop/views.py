from django.shortcuts import render, get_object_or_404
from .models import Category, Gloves


def index(request):
    post = 'Hello word'
    return render(request, 'index.html', {'post': post})


def product_list(request, category_slug):
    categories = Category.objects.filter(published=True)
    category = get_object_or_404(Category, slug=category_slug)
    products = Gloves.objects.filter(published=True)
    products = products.filter(category=category)

    return render(
        request, 'product/list_products.html', {
            'categories': categories,
            'category': category,
            'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Gloves, id=id, slug=slug, published=True)

    return render(
        request, 'product/detail_products.html', {'product': product})
