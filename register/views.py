from datetime import datetime, date
from django.db.models import Q
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.http import HttpResponse
from .forms import *
from .models import *
from payments.forms import RefundCreateForm, PaymentCreateForm
from payments.models import Refund, Payments

from .entities import extract_person, signatures


def index(request):
    return redirect("register:person", pk=0)
    # return HttpResponse("Hello, world. You're at the polls index.")


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def assign(request):
    signature = request.GET.get('signature', None)
    if not signature:
        return index(request)
    # case = get_object_or_404(Case, signature=signature)
    case = Case.objects.filter(signature=signature).first()
    if not case:
        return redirect('register:case', pk=0)

    accused_person = request.GET.get('accused_person', None)
    if accused_person:
        p = Person.objects.filter(pk=accused_person).first()
        if p:
            case.accused_persons.add(p)

    prosecutor_person = request.GET.get('prosecutor_person', None)
    if prosecutor_person:
        p = Person.objects.filter(pk=prosecutor_person).first()
        if p:
            case.prosecutor_persons.add(p)

    accused_company = request.GET.get('accused_company', None)
    if accused_company:
        c = Company.objects.filter(pk=accused_company).first()
        if c:
            case.accused_companies.add(c)

    prosecutor_company = request.GET.get('prosecutor_company', None)
    if prosecutor_company:
        c = Company.objects.filter(pk=prosecutor_company).first()
        if c:
            case.prosecutor_companies.add(c)
    case.save()
    return redirect('register:case', pk=case.pk)


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
            cases = Case.objects.filter(Q(accused_persons__pk=pk) | Q(prosecutor_persons__pk=pk))
            new_case_form = CaseForm(
                initial={
                    'accused_persons': find
                }
            )
            context = {
                'person': find,
                'family': ff,
                'new_case': new_case_form,
                'cases': cases,
                'next_signatures': signatures.next_signature(),
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
            person_id = form.cleaned_data.get('accused_persons').first().id
            form.save()
            return redirect("register:person", pk=person_id)
        return redirect("register:person", pk=0)
    if request.method == 'GET' and pk:
        context = {'case': Case.objects.get(pk=pk), 'refund': Refund.objects.filter(case__pk=pk).first()}
        if context['refund']:
            context['form'] = PaymentCreateForm(initial={'refund': context['refund']})
            context['payments'] = Payments.objects.filter(refund__pk=context['refund'].pk)
        else:
            context['form'] = RefundCreateForm(initial={'case': context['case']})
        return render(request, 'case/selected.html', context)

    context = {
        'cases': Case.objects.all()
    }
    return render(request, 'case/list.html', context)


def case_edit(request, pk=0):
    selected = Case.objects.get(pk=pk)
    form = CaseEditForm()
    context = {
        'form': form
    }
    return render(request, 'case/edit.html', context)


def bailiff(request):
    if request.method == 'POST':
        form = BailiffCreateForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': BailiffCreateForm,
        'bailiffs': Bailiff.objects.all()
    }
    return render(request, 'bailiff/bailiff.html', context)


def new_case(request):
    begin_of_month = date.today().replace(day=1)
    gen = Case.objects.filter(create_date__gte=begin_of_month).count() + 1
    form = CaseForm(request.POST,
                    initial={'signature': f'M/{datetime.now().strftime("%y")}/{gen}'}
                    )
    context = {
        'form': form
    }
    return render(request, 'case/create.html', context)


def assign_persons_to_case(persons, cases):
    c = Case.objects.filter(signature=cases.signature).first()
    if not c:
        c = cases
        c.save()

    for per in persons:
        p = Person.objects.filter(last_name=per.last_name, first_name=per.first_name).first()
        if not p:
            p = per
            p.save()
        c.persons.add(p)
    c.save()


def data_import(request):
    unassigned = ''
    if request.method == 'POST':
        form = ImportDataForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data.get('data').split(sep='\r\n')
            for row in rows:
                parts = row.split(sep='\t', maxsplit=2)
                if len(parts) < 3:
                    unassigned += 'za krótkie ' + row + '\r\n'
                    continue
                c = Case(signature=parts[1], description=parts[2])
                if parts[0].upper().find('SP. Z O.O.') > 0:
                    unassigned += row + '\r\n'
                else:
                    if len(parts[0].split(sep=',')) == 1:
                        person_data = parts[0].split(sep=' ', maxsplit=1)
                        if len(person_data) == 2:
                            p = Person(last_name=person_data[0], first_name=person_data[1])
                            assign_persons_to_case((p,), c)
                    else:
                        people = extract_person(parts[0])
                        assign_persons_to_case(people, c)

    context = {
        'form': ImportDataForm(initial={'data': unassigned})
    }
    return render(request, 'refactor/data_import.html', context)


def flush_data(request):
    Case.objects.all().delete()
    Person.objects.all().delete()
    return HttpResponse("Ucunięto wszystkie rekordy")


def company(request, pk=0):
    if request.method == 'POST':
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            new = form.save()
            return redirect('register:company', pk=new.pk)

    if request.method == 'GET':
        if pk > 0:
            context = {
                'company': Company.objects.filter(pk=pk).first(),
                'cases': Case.objects.filter(Q(accused_companies__pk=pk) | Q(prosecutor_companies__pk=pk))
            }
            return render(request, 'company/selected.html', context)
    context = {
        'new_company': CompanyCreateForm(),
        'companies': Company.objects.all()
    }
    return render(request, 'company/list.html', context)

