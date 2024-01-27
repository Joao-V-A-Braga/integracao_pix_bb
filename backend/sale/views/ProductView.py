from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from PIL import Image

from ..models.Product import Product
from ..forms.ProductForm import ProductForm
from ..serializers.ProductSerializer import ProductSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_products = Product.objects.all().order_by("id")
        
        result_page = paginator.paginate_queryset(all_products, request)

        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar os produtos cadastrados, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def create(request):
    try:
        productform = ProductForm(data=request.data, files=request.FILES)
        
        if productform.is_valid():
            productform.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(productform.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar cadastrar um novo produto, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['PUT'])
def update(request):
    try:
        try:
            product = Product.objects.get(id=request.data.get("id"))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        productSerialized = ProductSerializer(product)
        
        data = {**productSerialized.data, **request.data}
        productForm = ProductForm(data, instance=product)
        if productForm.is_valid():
            productForm.save()
            return Response(status=status.HTTP_200_OK)
        return Response(productForm.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar editar um produto, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['DELETE'])
def delete(request):
    try:
        try:
            product = Product.objects.get(id=request.data.get("id"))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Product.delete(product)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar deletar um produto, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )