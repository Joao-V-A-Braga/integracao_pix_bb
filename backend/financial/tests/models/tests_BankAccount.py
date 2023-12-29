from django.test import TestCase

from ...models.Bank import Bank
from ...models.BankAccount import BankAccount

class BankAccountTestCase(TestCase):
    bankName = "Banco do Brasil"
    bankCode = "001"

    def testBankAccountStrReturn(self):
        for data in self.dataProvider:
            bank = Bank(
                name=data['bank']['name'],
                code=data['bank']['code']
            )

            bankAccount = BankAccount(
                bank=bank,
                number=data['number'],
                agency=data['agency'],
                cnpj=data['cnpj']
            )

            self.assertEqual(
                bankAccount.__str__(), 
                f"{data['bank']['name']} {data['cnpj']}"
            )
    
    dataProvider = [
        {
            "message": "whenCnpjIsNone",
            "number": "12431234",
            "agency": "342234",
            "cnpj": None,
            "bank": {
                "name": bankName,
                "code": bankCode
            }
        },
        {
            "message": "whenNameOfBankIsNone",
            "number": "12431234",
            "agency": "342234",
            "cnpj": "61.015.142/0001-17",
            "bank": {
                "name": None,
                "code": bankCode
            }
        }
    ]