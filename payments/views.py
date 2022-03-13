from django.shortcuts import render, redirect
from django.http import Http404
from .models import *
from .forms import RefundCreateForm


def home(request):
    return Http404("nie ma takiego płacenia")


def refund(request, id=0):
    if request.method == 'POST':
        form = RefundCreateForm(request.POST)
        if form.is_valid():
            case = form.cleaned_data.get('case')
            form.save()
            return redirect('register:case', case.id)

    return Http404("nie przesłano prawidłowego formularza")
