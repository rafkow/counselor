from django.db import models
from register.models import Case


class Refund(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    court_costs = models.FloatField(null=False, default=0, verbose_name='koszty sądowe')
    clause_costs = models.FloatField(null=True, verbose_name='koszty klauzuli')
    interest = models.FloatField(null=True, verbose_name='odsetki')
    attorney_representation_costs = models.FloatField(null=True, verbose_name='koszty zast. w egz')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='klauzula sprawy')

    @property
    def amount(self):
        return self.court_costs + self.clause_costs + self.interest + self.attorney_representation_costs

    def recapitulation(self):
        payments = self.bill.all()
        if payments:
            return sum([p.value for p in payments])
        return 0

    def result(self):
        return self.amount - self.recapitulation()

    def __str__(self):
        return f"koszty {self.court_costs}"


class Payments(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(null=True)
    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name='bill')

