from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='imię')
    last_name = models.CharField(max_length=60, null=True, verbose_name='nazwisko')
    pesel = models.CharField(max_length=11, null=True, blank=True, verbose_name='numer pesel')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='numer telefonu')
    date_created = models.DateTimeField(auto_now_add=True)
    street = models.CharField(max_length=60, default='', verbose_name='ulica')
    city = models.CharField(max_length=60, default="Grudziądz", verbose_name='miejscowość')
    postcode = models.CharField(max_length=60, default='86-300', verbose_name='kod pocztowy')
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name='notatka')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Family(models.Model):
    name = models.CharField(max_length=200, verbose_name='nazwa rodziny')
    persons = models.ManyToManyField(Person, verbose_name='członkowie rodziny')

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='pełna nazwa podmiotu gospodarczego')
    nip = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='nip')
    krs = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name='notatki')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


# Komornik sądowy
class Bailiff(models.Model):
    name = models.CharField(max_length=60, verbose_name="imię i nazwisko")
    office_name = models.CharField(max_length=200, verbose_name='nazwa kancelarii', default='')
    street = models.CharField(max_length=60, default='', verbose_name='ulica')
    city = models.CharField(max_length=60, default="Grudziądz", verbose_name='miejscowość')
    postcode = models.CharField(max_length=60, default='86-300', verbose_name='kod pocztowy')

    def __str__(self):
        return f"{self.name}"


class Case(models.Model):
    # ('save value in DB', 'display on selected list')
    TYPE = (('eviction', 'eksmisja'), ('payment', 'o zapłatę'),
            ('divorce', 'rozwód'), ('insolvency', 'zgłoszenie wierzytenlość'))
    RESULT = (('new', 'nowa'),
              ('begin', 'rozpoczęta'),
              ('won', 'wygrana'),
              ('lose', 'przegrana'),
              ('enforced', 'egzekwowana'),
              ('end', 'zakończona'))


    signature = models.CharField(max_length=30, null=True, blank=True, unique=True,
                                 verbose_name='sygnatura kancelarii'
                                 )
    accused_persons = models.ManyToManyField(Person, related_name='accused_persons',
                                             verbose_name='osoby oskarżone w sprawie')
    accused_companies = models.ManyToManyField(Company, related_name='accused_companies',  blank=True)
    prosecutor_persons = models.ManyToManyField(Person, related_name='prosecutor_persons', blank=True)
    prosecutor_companies = models.ManyToManyField(Company, related_name='prosecutor_companies', blank=True)
    type = models.CharField(max_length=60, choices=TYPE, null=True, blank=True, verbose_name='typ sprawy', default=None)
    result = models.CharField(max_length=60, choices=RESULT, default=RESULT[0][0], verbose_name='wynik: sprawy')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    bailiff = models.ForeignKey(Bailiff, null=True, blank=True, verbose_name='komornik', on_delete=models.SET_NULL,
                                default=None)
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='opis', default=None)

    def __str__(self):
        return f"{self.signature}"


class Court(models.Model):
    case = models.ForeignKey(Case, verbose_name='sprawa', on_delete=models.CASCADE, null=False)
    court_id = models.IntegerField()
    signature = models.CharField(max_length=15)
    court_name = models.CharField(max_length=150)
    receipt_date = models.DateTimeField(verbose_name="data wpłynięcia sprawy")
    finish_date = models.DateTimeField(verbose_name="data zakończenia rozprawy", null=True)
    judge_name = models.CharField(max_length=150)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True)

    def init(self, portal_response=None):
        if portal_response:
            self.court_id = portal_response['id']
            self.signature = portal_response['signature']
            self.court_name = portal_response['courtName']
            self.receipt_date = portal_response['receiptDate']
            self.finish_date = portal_response['finishDate']
            self.judge_name = portal_response['judgeName']
            self.subject = portal_response['subject']
            self.description = portal_response['description']

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
