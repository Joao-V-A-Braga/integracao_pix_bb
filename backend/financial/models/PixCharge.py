from django.db import models
from django.core.validators import MinValueValidator

from .PixAccount import PixAccount

class PixCharge(models.Model):
    pixAccount = models.ForeignKey(PixAccount, on_delete=models.PROTECT)
    key = models.CharField()
    value = models.FloatField(validators=[MinValueValidator(0.01)])
    status = models.SmallIntegerField(default=1)
    expiration = models.PositiveIntegerField()
    code = models.CharField()
    txid = models.CharField()
    location = models.CharField()
    e2eid = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.value if self.value is not None and self.value >= 0.01 else 0.01} {self.status} {self.pixAccount.bankAccount.bank.name} {self.key}"