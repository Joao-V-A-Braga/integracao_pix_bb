from django.test import TestCase

from ...models.Bank import Bank
from ...models.BankAccount import BankAccount
from ...models.PixAccount import PixAccount

import time

class PixAccountTestCase(TestCase):

    bankAccount= {
        "number": "12431234",
        "agency": "342234",
        "cnpj": "61.015.142/0001-17",
    }
    
    bank= {
        "name": "Banco do Brasil",
        "code": "001"
    }

    def testPixStrReturn(self):
        for data in self.dataProviderPixKey:
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
            
            pixAccount = PixAccount(
                bankAccount=bankAccount,
                key=data['pixKey'],
                clientId="asfdsdafsadfas",
                secretId="hfdgsgfdsgfdsg",
                expire_time=time.gmtime()
            )

            self.assertEqual(
                pixAccount.__str__(), 
                f"{bank.name} {pixAccount.key}"
            )
    
    dataProviderPixKey = [
        {
            "message": "whenCnpjIsNone",
            "pixKey": None
        },
        {
            "message": "whenNameOfBankIsNone",
            "pixKey": "61.015.142/0001-17"
        },
        {
            "message": "whenNameOfBankIsNone",
            "pixKey": "dsfasdfjlkasdkfjçlasdfa"
        },
        {
            "message": "whenNameOfBankIsNone",
            "pixKey": "(62) 98177-6411"
        }
    ]