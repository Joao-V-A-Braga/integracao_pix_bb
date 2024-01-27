from django.contrib import admin

from .models.Product import Product

# Sale models registers
admin.site.register(Product)