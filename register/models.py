from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='imię')
    last_name = models.CharField(max_length=60, verbose_name='nazwisko')
    address = models.CharField(max_length=60, null=True, blank=True, verbose_name='adres')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='numer telefonu')
    date_created = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=30, null=True, blank=True, verbose_name='notatka')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Family(models.Model):
    name = models.CharField(max_length=200)
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return f"{self.name}"


# komornik
class Bailiff(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"


class Case(models.Model):
    # ('save value in DB', 'display on selected list')
    TYPE = (('eviction', 'eksmisja'), ('murder', 'morderstwo'))

    signature = models.CharField(max_length=30, null=True, blank=True, unique=True,
                                 verbose_name='sygnatura kancelarii'
                                 )
    persons = models.ManyToManyField(Person)
    type = models.CharField(max_length=60, choices=TYPE, null=True, blank=True, verbose_name='typ sprawy', default=None)
    result = models.CharField(max_length=60, blank=True, null=True, verbose_name='wynik sprawy')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    costs = models.FloatField(null=True, blank=True)
    bailiff = models.ForeignKey(Bailiff, null=True, blank=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return f"{self.signature}"


class Refund(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)




