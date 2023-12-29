from django.contrib import admin
from django.urls import path

from .views import BankView

urlpatterns = [
    #banks
    path('banks/', BankView.index, name='banks_index'),
]