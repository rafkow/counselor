from django.http import JsonResponse
from register.models import Person, Company
from django.views.decorators.csrf import csrf_exempt
from register.serializers import PersonSerializer, CompanySerializer


@csrf_exempt
def person(request):
    persons = Person.objects.all()
    serializer = PersonSerializer(persons, many=True)
    return JsonResponse(serializer.data, safe=False)


def company(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return JsonResponse(serializer.data, safe=False)

