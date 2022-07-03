from rest_framework import serializers
from register.models import Person, Company


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['id', 'first_name', 'last_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']



