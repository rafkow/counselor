from django.contrib import admin
from .models import Person, Case, Bailiff, Court, Company
from payments.models import Payments, Refund

admin.site.register(Person)
admin.site.register(Case)
admin.site.register(Bailiff)
admin.site.register(Court)
admin.site.register(Company)
admin.site.register(Payments)
admin.site.register(Refund)
