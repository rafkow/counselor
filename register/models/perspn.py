from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='imię')
    last_name = models.CharField(max_length=60, null=True, verbose_name='nazwisko')
    pesel = models.CharField(max_length=11, null=True, blank=True, verbose_name='numer pesel')
    address = models.CharField(max_length=60, null=True, blank=True, verbose_name='adres')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='numer telefonu')
    date_created = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=30, null=True, blank=True, verbose_name='notatka')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

