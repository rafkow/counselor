from django.urls import path
from . import views


app_name = 'payments'
urlpatterns = [
    path('', views.home, name='index'),
    path('refund', views.refund, name='refund'),
    path('refund/<int:id>', views.refund, name='refund'),
    path('payment', views.payment, name='payment'),
    path('generate', views.generate_enforcement_request, name='enforcement_request'),
    path('generate/<int:case_id>', views.generate_enforcement_request, name='enforcement_request'),
]


