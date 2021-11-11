from django.urls import path
from . import views


app_name = 'register'
urlpatterns = [
    path('', views.home, name='index'),
    path('person/create', views.create, name='create'),
    path('update/<int:pk>', views.update, name='update'),
    path('person', views.person, name='persons'),
    path('person/<int:pk>', views.person, name='person'),
    path('case/', views.case, name='case'),
    path('case/<int:pk>', views.case, name='case'),
    path('home/', views.home, name='home'),
    path('register/family', views.family, name='family'),
    path('import', views.data_import, name='data_import')
]
