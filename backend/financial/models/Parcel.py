from django.db import models
from .InvoiceToReceive import InvoiceToReceive

class Parcel(models.Model):
    invoiceToReceive = models.ForeignKey(InvoiceToReceive, on_delete=models.PROTECT)
    paymentDate = models.DateField()
    value = models.FloatField()
    status = models.PositiveSmallIntegerField()
    sequence = models.PositiveSmallIntegerField()
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"#{self.id} R${self.value}; {f'A vencer' if self.status == 1 else f'Pago em {self.paymentDate}'}"