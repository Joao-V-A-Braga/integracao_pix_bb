from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.ParcelPix import ParcelPix
from ..forms.PixChargeForm import PixChargeForm
from ..serializers.ParcelPixSerializer import ParcelPixSerializer

@api_view(['GET'])
def index(request):
    try:
        paginator = PageNumberPagination()
        
        all_parcel = ParcelPix.objects.all().order_by("id")
        
        result_page = paginator.paginate_queryset(all_parcel, request)

        serializer = ParcelPixSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response(
            f"\n\n{e}\n\nOcorreu um erro interno ao tentar buscar as parcelas, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['GET'])
def find(request, id):
    try:
        try:
            parcels = ParcelPix.objects.get(id=id)
        except ParcelPix.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParcelPixSerializer(parcels, many=False)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(
            "Ocorreu um erro interno ao tentar buscar as parcelas, por gentileza contacte o nosso suporte.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )