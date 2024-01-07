from django.test import TestCase

from ...models.ParcelPix import ParcelPix
from ...models.InvoiceToReceive import InvoiceToReceive
from ...models.Bank import Bank
from ...models.BankAccount import BankAccount

class ParcelPixTestCase(TestCase):

    def testParcelStrReturn(self):
        bank = Bank(
            name="Banco do Brasil",
            code="001"
        )

        bankAccount = BankAccount(
            bank=bank,
            number="12431234",
            agency="342234",
            cnpj="61.015.142/0001-17"
        )
        
        invoiceToReceive = InvoiceToReceive(
                id=1,
                bankAccount=bankAccount,
                quantityParcel=12,
                status=1,
                value=120
            )
        
        for data in self.dataProvider:
            parcel = ParcelPix(
                id=data['id'],
                paymentDate=data['paymentDate'],
                value=data['value'],
                sequence=1,
                status=data['status'],
                invoiceToReceive=invoiceToReceive
            )

            self.assertEqual(
                parcel.__str__(),
                f"#{data['id']} R${data['value']}; {f'A vencer' if data['status'] == 1 else f'Pago em {data['paymentDate']}'}",
                msg=data['message']
                )
    
    dataProvider = [
        {
            "message": "whenIsStatusToDue",
            "id": 1,
            "status": 1,
            "paymentDate": None,
            "value": 10
        },
        {
            "message": "whenIsStatusIsPaid",
            "id": 2,
            "status": 2,
            "paymentDate": "01/01/2024",
            "value": 10
        }
    ]