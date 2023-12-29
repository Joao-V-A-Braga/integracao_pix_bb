from django.contrib import admin
from django.urls import path

from .views import BankView

urlpatterns = [
    #banks
    path('banks/', BankView.index, name='banks_index'),
    path('banks/new', BankView.create, name='banks_create'),
    path('banks/update', BankView.update, name='banks_update'),
    path('banks/delete', BankView.delete, name='banks_delete'),
]