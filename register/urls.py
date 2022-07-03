from django.urls import path
from . import views, api


app_name = 'register'
urlpatterns = [
    path('', views.index, name='index'),
    path('person/create', views.create, name='create'),
    path('case/assign/', views.assign, name='assign'),
    path('update/<int:pk>', views.update, name='update'),
    path('person', views.person, name='persons'),
    path('person/<int:pk>', views.person, name='person'),
    path('case/', views.case, name='case'),
    path('case/<int:pk>', views.case, name='case'),
    path('register/family', views.family, name='family'),
    path('import', views.data_import, name='data_import'),
    path('flush', views.flush_data, name='flush'),
    path('bailiff', views.bailiff, name='bailiff'),
    path('company', views.company, name='company'),
    path('company/<int:pk>', views.company, name='company'),
    path('api/person', api.person, name='api_person'),
    path('api/company', api.company, name='api_company'),
]

handler404 = "register.views.page_not_found_view"