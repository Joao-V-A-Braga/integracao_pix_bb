from django.db import models
from .BankAccount import BankAccount

class PixAccount(models.Model):
    bankAccount = models.OneToOneField(
        BankAccount, on_delete=models.CASCADE, primary_key=True
        )
    key = models.CharField()
    clientId = models.CharField()
    secretId = models.CharField()
    expire_time = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bankAccount.bank.name} {self.key}"