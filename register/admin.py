from django.contrib import admin
from .models import *


admin.site.register(Person)
admin.site.register(Family)
admin.site.register(Case)
admin.site.register(Bailiff)

