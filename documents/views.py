from django.shortcuts import render
from .models import Document


def home(request):
    context = {
        'docs': Document.objects.all()
    }
    return render(request, 'documents.html', context)
