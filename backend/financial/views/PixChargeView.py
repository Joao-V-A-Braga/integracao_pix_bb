from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.PixCharge import PixCharge
from ..serializers.PixChargeSerializer import PixChargeSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_pix_charges = PixCharge.objects.all().order_by("id")
        
        result_page = paginator.paginate_queryset(all_pix_charges, request)

        serializer = PixChargeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar os pagamentos pix, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['GET'])
def find(request, id):
    try:
        try:
            pix_charge = PixCharge.objects.get(id=id)
        except PixCharge.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PixChargeSerializer(pix_charge, many=False)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar o pagamento pix, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )