from django.contrib import admin

from .models.Bank import Bank
from .models.BankAccount import BankAccount
from .models.PixAccount import PixAccount
from .models.PixCharge import PixCharge
from .models.InvoiceToReceive import InvoiceToReceive
from .models.ParcelPix import ParcelPix

# Financial models registers
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(PixAccount)
admin.site.register(PixCharge)
admin.site.register(InvoiceToReceive)
admin.site.register(ParcelPix)