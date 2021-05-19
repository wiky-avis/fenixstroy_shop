from django.shortcuts import render


def index(request):
    post = 'Hello word'
    return render(request, 'index.html', {'post': post})
