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


class Family(models.Model):
    name = models.CharField(max_length=200)
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='pełna nazwa podmiotu gospodarczego')
    nip = models.IntegerField(null=True, blank=True, verbose_name='nip')
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name='notatki')
    date_created = models.DateTimeField(auto_now_add=True)


# komornik
class Bailiff(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"


class Case(models.Model):
    # ('save value in DB', 'display on selected list')
    TYPE = (('eviction', 'eksmisja'), ('payment', 'o zapłatę'),
            ('divorce', 'rozwód'), ('insolvency', 'zgłoszenie wierzytenlość'))

    signature = models.CharField(max_length=30, null=True, blank=True, unique=True,
                                 verbose_name='sygnatura kancelarii'
                                 )
    accused_persons = models.ManyToManyField(Person, related_name='accused_persons', verbose_name='osoby oskarżone w sprawie')
    accused_companies = models.ManyToManyField(Company, related_name='accused_companies')
    prosecutor_persons = models.ManyToManyField(Person, related_name='prosecutor_persons')
    prosecutor_companies = models.ManyToManyField(Company, related_name='prosecutor_companies')
    type = models.CharField(max_length=60, choices=TYPE, null=True, blank=True, verbose_name='typ sprawy', default=None)
    result = models.CharField(max_length=60, blank=True, null=True, verbose_name='wynik sprawy')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    costs = models.FloatField(null=True, blank=True, default=0, verbose_name='koszty sprawy')
    bailiff = models.ForeignKey(Bailiff, null=True, blank=True, verbose_name='komornik', on_delete=models.SET_NULL, default=None)
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='opis', default=None)

    def __str__(self):
        return f"{self.signature}"


class Firstnames(models.Model):
    TYPE = (('male', 'mężczyzna'), ('female', 'kobieta'))
    name = models.CharField(max_length=60, unique=True, verbose_name='imię', default=None)
    gender = models.CharField(max_length=60, choices=TYPE, null=True, blank=True, verbose_name='płeć', default=None)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]




