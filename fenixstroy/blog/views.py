from django.shortcuts import render

# Create your views here.


def blog_list(request):
    return render(request, 'blog.html')


def blog_detail(request):
    return render(request, 'blog-details.html')
