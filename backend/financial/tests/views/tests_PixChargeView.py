from .BaseTestCaseView import BaseTestCaseView
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.BankAccount import BankAccount
from ...models.Bank import Bank
from ...models.PixAccount import PixAccount
from ...models.PixCharge import PixCharge

class PixChargeViewTestCase(BaseTestCaseView):
    
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

        PixCharge.objects.create(
            id=1,
            pixAccount=pixAccount,
            key="61.015.142/0001-17", value=10.15,
            status=1, expiration=1647838478, code="00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
            txid="fJrGXOYesIFHuUcRHGYndCev40", location="qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
            e2eid=None
        )

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get', 
            route_name='pix_charges_index'
        )

    @patch('financial.models.PixCharge.PixCharge.objects.all')
    def testContentOnIndexAction(self, mock_pix_charge:MagicMock):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_pix_charge, route='pix_charges_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=[
                "id", "pixAccount", "key", "value", "status", "expiration", "code",
                "txid", "location", "e2eid"
                ]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoPixCharges",
            "content": [
                {
                    "id": 1,
                    "pixAccount":PixAccount(
                        key='61.015.142/0001-56', clientId='asfdsafsadfty',
                        secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                        bankAccount=BankAccount(
                                id=1, number='12431234', agency='342234',
                                cnpj='61.015.142/0001-17', 
                                bank=Bank(id=1, name='Banco A', code="001")
                            )
                    ),
                    "key":"61.015.142/0001-17", "value":10.15,
                    "status":1, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                    "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                    "e2eid": None
                },
                {
                    "id": 2,
                    "pixAccount":PixAccount(
                        key='61.015.142/0001-56', clientId='asfdsafsadfty',
                        secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                        bankAccount=BankAccount(
                                id=1, number='12431234', agency='342234',
                                cnpj='61.015.142/0001-17', 
                                bank=Bank(id=1, name='Banco A', code="001")
                            )
                    ),
                    "key":"61.015.142/0001-17", "value":21.35,
                    "status":2, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                    "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                    "e2eid": "E0000000020231123181439303485326"
                },
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenPixCharges",
            "content": [
                {
                    "id": i,
                    "pixAccount":PixAccount(
                        key='61.015.142/0001-56', clientId='asfdsafsadfty',
                        secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                        bankAccount=BankAccount(
                                id=1, number='12431234', agency='342234',
                                cnpj='61.015.142/0001-17', 
                                bank=Bank(id=1, name='Banco A', code="001")
                            )
                    ),
                    "key":"61.015.142/0001-17", "value":21.35,
                    "status":2, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                    "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                    "e2eid": "E0000000020231123181439303485326"
                }
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenPixCharges",
            "content": [
                {
                    "id": i,
                    "pixAccount":PixAccount(
                        key='61.015.142/0001-56', clientId='asfdsafsadfty',
                        secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                        bankAccount=BankAccount(
                                id=1, number='12431234', agency='342234',
                                cnpj='61.015.142/0001-17', 
                                bank=Bank(id=1, name='Banco A', code="001")
                            )
                    ),
                    "key":"61.015.142/0001-17", "value":21.35,
                    "status":2, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                    "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                    "e2eid": "E0000000020231123181439303485326"
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
            route_name='pix_charges_find',
            path_attr={"id":1}
        )
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_404_NOT_FOUND, 
            method='get',
            route_name='pix_charges_find',
            path_attr={"id":2}
        )
    
    @patch('financial.models.PixCharge.PixCharge.objects.get')
    def testContentOnFind(self, mock_get:MagicMock):
        self.assertContentOnFindAction(
            mock_objects_get=mock_get, route='pix_charges_find',
            dataProvider=self.dataProviderContentFindAction,
            expectedAttrInResponse=[
                "id", "pixAccount", "key", "value", "status", "expiration", "code",
                "txid", "location", "e2eid"
                ],
            path_attr={"id":1}
            )
        
    dataProviderContentFindAction = [
        {
            "message": "whereE2eidIsNone",
            "content": {
                "id": 1,
                "pixAccount":PixAccount(
                    key='61.015.142/0001-56', clientId='asfdsafsadfty',
                    secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                    bankAccount=BankAccount(
                            id=1, number='12431234', agency='342234',
                            cnpj='61.015.142/0001-17', 
                            bank=Bank(id=1, name='Banco A', code="001")
                        )
                ),
                "key":"61.015.142/0001-17", "value":10.15,
                "status":1, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                "e2eid": None
            }
        },
        {
            "message": "whereE2eidIsNotNone",
            "content": {
                "id": 1,
                "pixAccount":PixAccount(
                    key='61.015.142/0001-56', clientId='asfdsafsadfty',
                    secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                    bankAccount=BankAccount(
                            id=1, number='12431234', agency='342234',
                            cnpj='61.015.142/0001-17', 
                            bank=Bank(id=1, name='Banco A', code="001")
                        )
                ),
                "key":"61.015.142/0001-17", "value":10.15,
                "status":1, "expiration": 1647838478, "code": "00020101021226870014br.gov.bcb.pix2565qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376520400005303986540540.005802BR5921PAPELARIA LEITE CUNHA6008BRASILIA62070503***63044B21",
                "txid":"fJrGXOYesIFHuUcRHGYndCev40", "location": "qrcodepix-h.bb.com.br/pix/v2/80e04cc4-c793-4f83-8c0a-2e200c4d7376",
                "e2eid": "E0000000020231123181439303485326"
            }
        }
    ]