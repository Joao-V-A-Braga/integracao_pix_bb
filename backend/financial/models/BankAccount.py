from django.db import models
from .Bank import Bank

class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    number = models.PositiveIntegerField()
    agency = models.PositiveIntegerField()
    cnpj = models.CharField(max_length=18)

    def __str__(self):
        return f"{self.bank.name} {self.cnpj}"