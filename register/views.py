from datetime import datetime, date
from django.shortcuts import render, redirect
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


def family(request):
    if request.method == 'POST':
        form = FamilyCreateForm(request.POST)
        if form.is_valid():
            person_id = form.cleaned_data.get('persons').first().id
            form.save()
            return redirect("register:person", pk=person_id)
    return redirect("person", pk=0)


def create(request):
    if request.method == 'POST':
        form = PersonCreateFrom(request.POST)
        if form.is_valid():
            new = form.save()
            return redirect('register:person', pk=new.pk)
        return redirect('register:persons')
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
            return redirect("person", pk=new.pk)
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
    if request.method == 'GET':
        if pk:
            find = Person.objects.get(pk=pk)
            ff = Family.objects.filter(persons=find)
            if ff.count() < 1:
                ff = FamilyCreateForm(
                    initial={
                        'name': f'{find.last_name} - {find.address}',
                        'persons': find
                    }
                )
            begin_of_month = date.today().replace(day=1)
            gen = Case.objects.filter(create_date__gte=begin_of_month).count()+1
            cases = Case.objects.filter(persons__pk=pk)
            new_case_form = CaseForm(
                initial={
                    'signature': f'M/{datetime.now().strftime("%y/%m")}/{gen}',
                    'persons': find
                }
            )
            context = {
                'person': find,
                'family': ff,
                'new_case': new_case_form,
                'cases': cases,
            }
            return render(request, 'person/selected.html', context)
        else:
            context = {
                'persons': Person.objects.all()
            }
            return render(request, 'person/list.html', context)


def case(request, pk=0):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            person_id = form.cleaned_data.get('persons').first().id
            form.save()
            return redirect("register:person", pk=person_id)
        return redirect("register:person", pk=0)
    if request.method == 'GET':
        if pk:
            selected = Case.objects.get(pk=pk)
            context = {
                'case': selected
            }
            return render(request, 'case/selected.html', context)

    begin_of_month = date.today().replace(day=1)
    gen = Case.objects.filter(create_date__gte=begin_of_month).count()+1
    form = CaseForm(request.POST,
                    initial={'signature': f'M/{datetime.now().strftime("%y/%m")}/{gen}'}
                    )
    context = {
        'form': form
    }
    return render(request, 'case/create.html', context)


def data_import(request):
    context = {
        'form': ImportDataForm
    }
    return render(request, 'refactor/data_import.html', context)




