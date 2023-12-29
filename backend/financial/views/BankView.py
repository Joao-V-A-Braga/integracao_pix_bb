from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

from ..models.Bank import Bank
from ..serializers.BankSerializer import BankSerializer

@api_view(['GET'])
def index(request):
    paginator = PageNumberPagination()
    
    all_banks = Bank.objects.all().order_by("name")
    
    result_page = paginator.paginate_queryset(all_banks, request)

    serializer = BankSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)