from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import *
from payments.forms import RefundCreateForm, PaymentCreateForm
from register.models import Case
from docx import Document


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


def payment(request):
    if request.method == 'POST':
        form = PaymentCreateForm(request.POST)
        if form.is_valid():
            bill = form.cleaned_data.get('refund')
            form.save()
            return redirect('register:case', bill.case.id)
    return Http404("nie przesłano prawidłowego formularza")


def generate_enforcement_request(request, case_id):
    document = Document('payments/resources/wszczecie_egzekucji_copy.docx')
    if selected_case:= Case.objects.get(id=case_id):
        for i, p in enumerate(document.paragraphs):
            for j, r in enumerate(p.runs):
                print(f"{i} {j} | {r.text}")
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=wszczęcie_egzekucji_{selected_case.signature}.docx'
        document.save(response)

    return response

