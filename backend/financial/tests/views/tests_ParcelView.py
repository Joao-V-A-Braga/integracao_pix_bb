from .BaseTestCaseView import BaseTestCaseView
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.BankAccount import BankAccount
from ...models.Bank import Bank
from ...models.PixAccount import PixAccount
from ...models.PixCharge import PixCharge
from ...models.ParcelPix import ParcelPix
from ...models.InvoiceToReceive import InvoiceToReceive

class ParcelViewTestCase(BaseTestCaseView):
    
    def setUp(self):
        bank = Bank.objects.create(name='Banco A', code="001")
        bankAccount = BankAccount.objects.create(
            id=1,
            number='12431256', agency='342256',
            cnpj='61.015.142/0001-18', 
            bank=bank
            )
        pixAccount = PixAccount.objects.create(
            key='61.015.142/0001-56', clientId='asfdsafsadfty',
            secretId='hfdgsgfdsgfcv', expire_time=1647838478,
            bankAccount=bankAccount
        )

        pixCharge = PixCharge.objects.create(
            id=1, pixAccount=pixAccount, key="61.015.142/0001-17", value=10.15,
            status=1, expiration=1647838478, code="00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
            txid="fJrGXOYesIFHuUcRHGYndCev40", location="qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
            e2eid=None
        )
        
        invoiceToReceive = InvoiceToReceive.objects.create(
                id=1,
                bankAccount=bankAccount,
                quantityParcel=12,
                status=1,
                value=120
            )
        
        ParcelPix.objects.create(
            id=1, pixCharge=pixCharge, invoiceToReceive=invoiceToReceive,
            paymentDate="2024-01-01", value=34.22,
            sequence=1, status=2
        )

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get',
            route_name='parcels_index'
        )

    @patch('financial.models.ParcelPix.ParcelPix.objects.all')
    def testContentOnIndexAction(self, mock_parcel:MagicMock):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_parcel, route='parcels_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=[
                "id", "pixCharge", "invoiceToReceive", "paymentDate", "status", 
                "value", "sequence"
                ]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoParcelPix",
            "content": [
                {
                    "id": 1, "pixCharge":PixCharge(id=1), "sequence": 1,
                    "invoiceToReceive":InvoiceToReceive(id=1),
                    "paymentDate":"01/01/2024", "value":10.15, "status":2,
                },
                {
                    "id": 2, "pixCharge":PixCharge(id=2), "sequence": 2,
                    "invoiceToReceive":InvoiceToReceive(id=1),
                    "paymentDate":None, "value":55.99, "status":1,
                },
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenParcelPix",
            "content": [
                {
                    "id": i, "pixCharge":PixCharge(id=i), "sequence": i,
                    "invoiceToReceive":InvoiceToReceive(id=i),
                    "paymentDate":"01/01/2024", "value":10.15, "status":2,
                }
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenPixCharges",
            "content": [
                {
                    "id": i, "pixCharge":PixCharge(id=i), "sequence": i,
                    "invoiceToReceive":InvoiceToReceive(id=i),
                    "paymentDate":"01/01/2024", "value":33.12, "status":2,
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
            route_name='parcels_find',
            path_attr={"id":1}
        )
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_404_NOT_FOUND, 
            method='get',
            route_name='parcels_find',
            path_attr={"id":2}
        )
    
    @patch('financial.models.ParcelPix.ParcelPix.objects.get')
    def testContentOnFind(self, mock_get:MagicMock):
        self.assertContentOnFindAction(
            mock_objects_get=mock_get, route='parcels_find',
            dataProvider=self.dataProviderContentFindAction,
            expectedAttrInResponse=[
                "id", "pixCharge", "invoiceToReceive", "paymentDate", "status", 
                "value", "sequence"
                ],
            path_attr={"id":1}
            )

    dataProviderContentFindAction = [
        {
            "message": "whenPaymentDateIsNone",
            "content": {
                "id": 1, "pixCharge":PixCharge(id=1), "sequence": 1,
                "invoiceToReceive":InvoiceToReceive(id=1),
                "paymentDate":"01/01/2024", "value":10.15, "status":2,
            },
        },
        {
            "message": "whenPaymentDateIsNotNone",
            "content": {
                "id": 1, "pixCharge":PixCharge(id=1), "sequence": 1,
                "invoiceToReceive":InvoiceToReceive(id=1),
                "paymentDate":None, "value":10.15, "status":1,
            },
        }
    ]