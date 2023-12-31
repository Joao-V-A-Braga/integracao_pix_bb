from django.contrib import admin

from .models.Bank import Bank
from .models.BankAccount import BankAccount
from .models.PixAccount import PixAccount

# Financial models registers
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(PixAccount)