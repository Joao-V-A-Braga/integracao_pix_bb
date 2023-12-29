from django.contrib import admin

from .models.Bank import Bank
from .models.BankAccount import BankAccount

# Financial models registers
admin.site.register(Bank)
admin.site.register(BankAccount)