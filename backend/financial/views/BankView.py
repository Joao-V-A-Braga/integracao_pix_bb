from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.Bank import Bank
from ..forms.BankForm import BankForm
from ..serializers.BankSerializer import BankSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_banks = Bank.objects.all().order_by("name")
        
        result_page = paginator.paginate_queryset(all_banks, request)

        serializer = BankSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar os bancos cadastrados, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def create(request):
    try:
        bankform = BankForm(request.data)
        if bankform.is_valid():
            bankform.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(bankform.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar cadastrar um novo banco, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['PUT'])
def update(request):
    try:
        try:
            bank = Bank.objects.get(id=request.data.get("id"))
        except Bank.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bankSerialized = BankSerializer(bank)
        
        data = {**bankSerialized.data, **request.data}
        bankform = BankForm(data, instance=bank)
        if bankform.is_valid():
            bankform.save()
            return Response(status=status.HTTP_200_OK)
        return Response(bankform.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar editar um banco, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['DELETE'])
def delete(request):
    try:
        try:
            bank = Bank.objects.get(id=request.data.get("id"))
        except Bank.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Bank.delete(bank)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar deletar um banco, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )