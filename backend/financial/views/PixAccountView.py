from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.PixAccount import PixAccount
from ..forms.PixAccountForm import PixAccountForm
from ..serializers.PixAccountSerializer import PixAccountSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_pix_accounts = PixAccount.objects.all().order_by("bankAccount")
        
        result_page = paginator.paginate_queryset(all_pix_accounts, request)

        serializer = PixAccountSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar buscar as contas pix cadastradas, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def create(request):
    try:
        pixAccountForm = PixAccountForm(request.data)
        if pixAccountForm.is_valid():
            pixAccountForm.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(pixAccountForm.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar cadastrar uma nova conta pix, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['PUT'])
def update(request):
    try:
        pixAccount = PixAccount.objects.get(bankAccount=request.data.get("bankAccount"))
        if not pixAccount:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pixAccountSerialized = PixAccountSerializer(pixAccount)

        data = {
            **pixAccountSerialized.data, 'secretId':pixAccount.secretId, 
            **request.data
            }

        pixAccountForm = PixAccountForm(data, instance=pixAccount)
        if pixAccountForm.is_valid():
            pixAccountForm.save()
            return Response(status=status.HTTP_200_OK)
        return Response(pixAccountForm.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar editar uma conta pix, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['DELETE'])
def delete(request):
    try:
        pixAccount = PixAccount.objects.get(bankAccount=request.data.get("bankAccount"))
        if not pixAccount:
            return Response(status=status.HTTP_404_NOT_FOUND)

        PixAccount.delete(pixAccount)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar deletar uma conta pix, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )