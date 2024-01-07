from django.db import models
from .BankAccount import BankAccount

class InvoiceToReceive(models.Model):
    bankAccount = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    status = models.SmallIntegerField()
    value = models.FloatField()
    quantityParcel = models.PositiveIntegerField()

    def __str__(self):
        return f"#{self.id} R${self.value} em {self.quantityParcel} vezes, para {self.bankAccount.bank.name}."