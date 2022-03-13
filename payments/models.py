from django.db import models
from register.models import Case


class Refund(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    court_costs = models.FloatField(null=False, default=0, verbose_name='koszty sądowe')
    clause_costs = models.FloatField(null=True, verbose_name='koszty klauzuli')
    interest = models.FloatField(null=True, verbose_name='odsetki')
    attorney_representation_costs = models.FloatField(null=True, verbose_name='koszty zast. w egz')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='klauzula sprawy')

    def __str__(self):
        return f"koszty {self.court_costs}"


class Payments(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(null=True)
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE)

