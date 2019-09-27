from django.http import JsonResponse
from django.shortcuts import render
from .forms import ReservationForm
from .models import Price


def home(request):
    if request.method == 'POST':
        return reservation(request)

    context = {
        'prices': Price.objects.all(),
        'range': range(1, 11)
    }
    return render(request, 'prices.html', context)


def reservation(request):
    form = ReservationForm(request.POST)
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
