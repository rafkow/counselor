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
from portal_informacyjny.portal import Portal
from .entities import extract_person, signatures
import json


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


def person(request, pk=0):
    if request.method == 'GET':
        if pk:
            find = Person.objects.get(pk=pk)
            ff = Family.objects.filter(persons=find)
            if ff.count() < 1:
                ff = FamilyCreateForm(
                    initial={
                        'name': f'{find.last_name} - {find.street}',
                        'persons': find
                    }
                )
            cases = Case.objects.filter(Q(accused_persons__pk=pk) | Q(prosecutor_persons__pk=pk))
            # new_case_form = CaseForm(
            #     initial={
            #         'accused_persons': find
            #     }
            # )
            context = {
                'person': find,
                'family': ff,
                # 'new_case': new_case_form,
                'simple_case_form': SimpleCaseCreateForm,
                'cases': cases,
                'next_signatures': signatures.next_signature(),
            }
            return render(request, 'person/selected.html', context)
        else:
            context = {
                'persons': Person.objects.all(),
                'form': PersonCreateFrom()
            }
            return render(request, 'person/list.html', context)
    if request.method == 'POST':
        form = PersonCreateFrom(request.POST)
        if form.is_valid():
            new = form.save()
            return redirect('register:person', pk=new.pk)
        return redirect('register:persons')


def person_update(request, pk):
    find = Person.objects.get(pk=pk)
    if request.method == 'POST':
        form = PersonCreateFrom(request.POST, instance=find)
        if form.is_valid():
            form.save()
        return redirect("register:person", pk=find.pk)
    if request.method == 'GET':
        form = PersonUpdateForm(instance=find)
        context = {
            'form': form
        }
        return render(request, 'person/update.html', context)


def case(request, pk=0):
    if request.method == 'POST':
        if pk:
            if selected_case := Case.objects.get(pk=pk):
                form = CaseNoteForm(request.POST, instance=selected_case)
                print('jestem w case')
                if form.is_valid():
                    form.save()
                return redirect("register:case", pk=selected_case.id)
        form = CaseForm(request.POST)
        if form.is_valid():
            person_id = form.cleaned_data.get('accused_persons').first().id
            form.save()
            return redirect("register:person", pk=person_id)
        return redirect("register:person", pk=0)
    if request.method == 'GET' \
        and request.GET.get('signature', None) \
        and request.GET.get('person_id', None) \
        and request.GET.get('type', None):
            signature = request.GET.get('signature', None)
            person_id = request.GET.get('person_id', None)
            type = request.GET.get('type', None)
            person = Person.objects.get(pk=person_id)
            case = Case(signature=signature, type=type)
            case.save()
            case.accused_persons.add(person)
            case.save()
            pk = case.pk
    if request.method == 'GET' and pk:
        if selected_case := Case.objects.get(pk=pk):
            if selected_case.result == 'begin':
                court_refresh(pk)
            context = {'case': selected_case, 'refund': Refund.objects.filter(case__pk=pk).first()}
            if context['refund']:
                context['form'] = PaymentCreateForm(initial={'refund': context['refund']})
                context['payments'] = Payments.objects.filter(refund__pk=context['refund'].pk)
            else:
                context['form'] = RefundCreateForm(initial={'case': context['case']})
            if court := Court.objects.get(case__pk=pk):
                context['court'] = court
                if not selected_case.bailiff:
                    context['assign_bailiff_form'] = CaseAssignBailiffForm()
            else:
                context['cort_reference_number_form'] = CaseCourtReferenceForm({'pk': selected_case.pk})
            context['case_note_form'] = CaseNoteForm(instance=selected_case)
            return render(request, 'case/selected.html', context)

    context = {
        'cases': Case.objects.all()
    }
    return render(request, 'case/list.html', context)


def case_update_court_reference_number(request, case_id = 0):
    if pk := request.GET.get('pk', case_id):
        if case_selected := Case.objects.get(pk=pk):
            if reference_number := request.GET.get('court_reference_number', None):
                result = Portal.get_case_by_court_reference_number(reference_number)
                result_dict = json.dumps(result[0])
                portal_response = json.loads(result_dict)
                court = Court()
                court.case = case_selected
                court.init(portal_response=portal_response)
                if court.finish_date:
                    case_selected.result = 'won'
                else:
                    case_selected.result = 'begin'
                case_selected.save()
                court.save()
    return redirect('register:case', pk=pk)


def court_refresh(case_id):
    if court := Case.objects.get(pk=case_id).court.get():
        if not court.finish_date:
            result = Portal.get_case_by_court_reference_number(court.signature)
            result_dict = json.dumps(result[0])
            portal_response = json.loads(result_dict)
            result_court = Court()
            result_court.init(portal_response=portal_response)
            if court < result_court:
                court.finish_date = result_court.finish_date
                court.save()
                selected_case = Case.objects.get(pk=case_id)
                selected_case.result = 'won'
                selected_case.save()


def case_court_info(request, pk=0):
    if case_selected := Case.objects.first(pk=pk):
        case_selected.court_reference_number
        Portal.get_case_by_court_reference_number(case_selected.court_reference_number)
    return redirect('register:case', pk=pk)
    

# def case_edit(request, pk=0):
#     selected = Case.objects.get(pk=pk)
#     form = CaseEditForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'case/edit.html', context)

def case_bailiff_assign(request):
    if request.method == 'POST':
        form = CaseAssignBailiffForm(request.POST)
        if form.is_valid():
            case_id = form.cleaned_data.get('id')
            find = Case.objects.get(pk=case_id)
            bailiff_id = form.cleaned_data.get('bailiff')
    if request.method == 'GET':
        case_id = request.GET.get('case_id', None)
        found_case = Case.objects.get(pk=case_id)
        if found_case:
            bailiff_id = request.GET.get('bailiff', None)
            found_bailiff = Bailiff.objects.get(pk=bailiff_id)
            if found_bailiff:
                found_case.bailiff = found_bailiff
                found_case.result = Case.RESULT[4][0]
                found_case.save()
                return redirect('register:case', pk=case_id)
    return redirect('register:case')


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

