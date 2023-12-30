from django.contrib import admin
from django.urls import path

from .views import BankView
from .views import BankAccountView

urlpatterns = [
    #banks
    path('banks/', BankView.index, name='banks_index'),
    path('banks/new', BankView.create, name='banks_create'),
    path('banks/update', BankView.update, name='banks_update'),
    path('banks/delete', BankView.delete, name='banks_delete'),
    
    #bank accounts
    path('bank-accounts/', BankAccountView.index, name='bank_accounts_index'),
    path('bank-accounts/new', BankAccountView.create, name='bank_accounts_create'),
    path('bank-accounts/update', BankAccountView.update, name='bank_accounts_update'),
    path('bank-accounts/delete', BankAccountView.delete, name='bank_accounts_delete'),
]