from django.shortcuts import render
from .models import *


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'projects/home.html', context)


def about(request):
    return render(request, 'projects/about.html', {'title': 'About'})
