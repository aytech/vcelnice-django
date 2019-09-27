from django.http import JsonResponse
from django.shortcuts import render
from .forms import ContactForm


def home(request):
    if request.method == 'POST':
        return contact(request)

    context = {
        'form': ContactForm()
    }
    return render(request, 'contact.html', context)


def contact(request):
    form = ContactForm(request.POST)
    response = {
        'success': False,
        'message': None
    }

    if form.is_valid():
        response['success'] = True
        form.save()
    else:
        errors = form.errors.as_data()
        for error in errors:
            response['message'] = ''.join(errors[error][0])
            break

    return JsonResponse(response)
