from django.shortcuts import render
from .models import Photo


def home(request):
    context = {
        'gallery': Photo.objects.all()
    }
    return render(request, 'photo.html', context)
