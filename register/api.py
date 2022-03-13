import requests
from django.http import HttpResponse, JsonResponse
from register.models import Person

from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def person(request):

    # persons = Person.objects.filter(pk__gt=0)
    # result = list()
    # for p in persons:
    #     result.append({"name": f"{p}", "id": p.pk})
    # data = json.dumps(result)

    data = Person.objects.first()
    data = model_to_dict(data)
    return JsonResponse(data)

