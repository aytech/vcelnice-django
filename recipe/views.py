from django.shortcuts import render
from .models import Recipe


def home(request):
    context = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'recipe.html', context)
