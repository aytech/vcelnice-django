from django.shortcuts import render
from .models import Article


def home(request):
    context = {
        'news': Article.objects.all()
    }
    return render(request, "news.html", context)
