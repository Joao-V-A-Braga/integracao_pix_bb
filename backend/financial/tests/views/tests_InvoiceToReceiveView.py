from .BaseTestCaseView import BaseTestCaseView
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.BankAccount import BankAccount
from ...models.Bank import Bank
from ...models.PixAccount import PixAccount
from ...models.PixCharge import PixCharge
from ...models.ParcelPix import ParcelPix
from ...models.InvoiceToReceive import InvoiceToReceive

class InvoiceToReceiveViewTestCase(BaseTestCaseView):
    
    def setUp(self):
        bank = Bank.objects.create(name='Banco A', code="001")
        bankAccount = BankAccount.objects.create(
            id=1, number='12431256', agency='342256', cnpj='61.015.142/0001-18', 
            bank=bank
            )
        
        InvoiceToReceive.objects.create(
            id=1, bankAccount=bankAccount, quantityParcel=12, status=1, value=120
            )

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get',
            route_name='invoice_to_receive_index'
        )

    @patch('financial.models.InvoiceToReceive.InvoiceToReceive.objects.all')
    def testContentOnIndexAction(self, mock_parcel:MagicMock):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_parcel, route='invoice_to_receive_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=[
                "id", "bankAccount", "quantityParcel", "status", "value"
                ]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoInvoiceToReceives",
            "content": [
                {
                    "id": 1, "bankAccount":BankAccount(id=1), "quantityParcel": 12,
                    "status":1, "value":2341.99
                },
                {
                    "id": 2, "bankAccount":BankAccount(id=2), "quantityParcel": 6,
                    "status":1, "value":2341.99
                },
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenParcelPix",
            "content": [
                {
                    "id": i, "bankAccount":BankAccount(id=i), "quantityParcel": i,
                    "status":1, "value":2341.99
                }
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenPixCharges",
            "content": [
                {
                    "id": i, "bankAccount":BankAccount(id=i), "quantityParcel": i,
                    "status":1, "value":2341.99
                }
                for i in range(1, 25)
            ],
            "expectedQtt": 24
        }
    ]

    # Find -----------------------------------------------
    def testStatusCodeOnFindAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get',
            route_name='invoice_to_receive_find',
            path_attr={"id":1}
        )
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_404_NOT_FOUND, 
            method='get',
            route_name='invoice_to_receive_find',
            path_attr={"id":2}
        )
    
    @patch('financial.models.InvoiceToReceive.InvoiceToReceive.objects.get')
    def testContentOnFind(self, mock_get:MagicMock):
        self.assertContentOnFindAction(
            mock_objects_get=mock_get, route='invoice_to_receive_find',
            dataProvider=self.dataProviderContentFindAction,
            expectedAttrInResponse=[
                "id", "bankAccount", "quantityParcel", "status", "value"
                ],
            path_attr={"id":1}
            )

    dataProviderContentFindAction = [
        {
            "message": "dataToFindInvoiceToReceive",
            "content": {
                "id": 1, "bankAccount":BankAccount(id=1), "quantityParcel": 12,
                "status":1, "value":2341.99
            },
        }
    ]