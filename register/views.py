from datetime import datetime, date

import requests
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.http import HttpResponse
from .forms import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    context = {
        'persons': Person.objects.all()
    }
    return render(request, 'person/list.html', context)


def create(request):
    if request.method == 'GET':
        form = PersonCreateFrom()
        context = {
            'form': form
        }
        return render(request, 'person/create.html', context)


def update(request, pk):
    if request.method == 'POST':
        form = PersonCreateFrom(request.POST)
        if form.is_valid():
            new = form.save()
            return person(request, new.pk)
    if request.method == 'GET':
        form = PersonCreateFrom()
        if pk:
            print(pk)
            find = Person.objects.get(pk=pk)
            print(f'osoba  {find}')
        context = {
            'form': form
        }
        return render(request, 'person/update.html', context)


def person(request, pk=0):
    print(pk)
    if request.method == 'GET':
        if pk:
            find = Person.objects.get(pk=pk)
            ff = FamilyCreateForm()
            context = {
                'person': find,
                'family': ff
            }
            return render(request, 'person/selected.html', context)
        else:
            context = {
                'persons': Person.objects.all()
            }
            return render(request, 'person/list.html', context)


def case(request, pk=0):
    if request.method == 'POST':
        return render(request, 'home.html')
    if request.method == 'GET':
        if pk:
            selected = Case.objects.get(pk=pk)
            context = {
                'case': selected
            }
            return render(request, 'case/selected.html', context)

    begin_of_month = date.today().replace(day=1)
    gen = Case.objects.filter(create_date__gte=begin_of_month).count()
    form = CaseForm(request.POST,
                    initial={'signature': f'M/{datetime.now().strftime("%y/%m")}/{gen}'}
                    )
    context = {
        'form': form
    }
    return render(request, 'case/create.html', context)

