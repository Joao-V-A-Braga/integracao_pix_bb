from django.urls import path

from .views import ProductView

urlpatterns = [
    path('products/', ProductView.index, name='products_index'),
    path('products/create', ProductView.create, name='products_create'),
    path('products/update', ProductView.update, name='products_update'),
    path('products/delete', ProductView.delete, name='products_delete'),
]