from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.InvoiceToReceive import InvoiceToReceive
from ..serializers.InvoiceToReceiveSerializer import InvoiceToReceiveSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_invoices_to_receive = InvoiceToReceive.objects.all().order_by("id")
        
        result_page = paginator.paginate_queryset(all_invoices_to_receive, request)

        serializer = InvoiceToReceiveSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar as contas a receber, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['GET'])
def find(request, id):
    try:
        try:
            invoice_to_receive = InvoiceToReceive.objects.get(id=id)
        except InvoiceToReceive.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceToReceiveSerializer(invoice_to_receive, many=False)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar a conta a receber, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )