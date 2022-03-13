from django.urls import path
from . import views


app_name = 'payments'
urlpatterns = [
    path('', views.home, name='index'),
    path('refund', views.refund, name='refund'),
    path('refund/<int:id>', views.refund, name='refund'),
]
