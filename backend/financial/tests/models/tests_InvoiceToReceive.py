from django.test import TestCase

from ...models.InvoiceToReceive import InvoiceToReceive
from ...models.Bank import Bank
from ...models.BankAccount import BankAccount

class InvoiceToReceiveTestCase(TestCase):

    def testInvoiceToReceiveStrReturn(self):
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
        
        for data in self.dataProvider:
            invoiceToReceive = InvoiceToReceive(
                id=data['id'],
                bankAccount=bankAccount,
                quantityParcel=data['quantityParcel'],
                status=1,
                value=data['value']
            )
            self.assertEqual(
                invoiceToReceive.__str__(),
                f"#{data['id']} R${data['value']} em {data['quantityParcel']} vezes, para {bank.name}.",
                msg=data['message']
                )
    
    dataProvider = [
        {
            "message": "whenIsFull",
            "id": 1,
            "value": 10.50,
            "quantityParcel": 12
        }
    ]