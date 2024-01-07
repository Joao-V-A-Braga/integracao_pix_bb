from django.contrib import admin
from django.urls import path

from .views import BankView
from .views import BankAccountView
from .views import PixAccountView
from .views import PixChargeView

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
    
    #pix accounts
    path('pix-accounts/', PixAccountView.index, name='pix_accounts_index'),
    path('pix-accounts/new', PixAccountView.create, name='pix_accounts_create'),
    path('pix-accounts/update', PixAccountView.update, name='pix_accounts_update'),
    path('pix-accounts/delete', PixAccountView.delete, name='pix_accounts_delete'),
    
    #pix charges
    path('pix-charges/', PixChargeView.index, name='pix_charges_index'),
    path('pix-charges/<int:id>', PixChargeView.find, name='pix_charges_find'),
]