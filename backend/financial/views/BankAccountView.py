from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.BankAccount import BankAccount
from ..forms.BankAccountForm import BankAccountForm
from ..serializers.BankAccountSerializer import BankAccountSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_bank_accounts = BankAccount.objects.all().order_by("id")
        
        result_page = paginator.paginate_queryset(all_bank_accounts, request)

        serializer = BankAccountSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(
            f"Ocorreu um erro interno ao tentar buscar as contas bancarias cadastradas, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def create(request):
    try:
        bankAccountForm = BankAccountForm(request.data)
        if bankAccountForm.is_valid():
            bankAccountForm.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(bankAccountForm.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar cadastrar uma nova conta bancária, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['PUT'])
def update(request):
    try:
        try:
            bankAccount = BankAccount.objects.get(id=request.data.get("id"))
        except BankAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        bankAccountSerialized = BankAccountSerializer(bankAccount)
        
        data = {**bankAccountSerialized.data, **request.data}
        bankAccountForm = BankAccountForm(data, instance=bankAccount)
        if bankAccountForm.is_valid():
            bankAccountForm.save()
            return Response(status=status.HTTP_200_OK)
        return Response(bankAccountForm.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar editar uma conta bancária, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['DELETE'])
def delete(request):
    try:
        try:
            bankAccount = BankAccount.objects.get(id=request.data.get("id"))
        except BankAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        BankAccount.delete(bankAccount)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar deletar uma conta bancária, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )