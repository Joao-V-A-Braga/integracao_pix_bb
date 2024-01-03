from django.test import TestCase

from ...models.Bank import Bank
from ...models.BankAccount import BankAccount
from ...models.PixAccount import PixAccount

import time

class PixAccountTestCase(TestCase):

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
                f"{bank.name} {data['pixKey']}"
            )
    
    dataProviderPixKey = [
        {
            "message": "whenPixKeyIsNone",
            "pixKey": None
        },
        {
            "message": "whenPixKeyACnpj",
            "pixKey": "61.015.142/0001-17"
        },
        {
            "message": "whenPixKeyIsWhatever",
            "pixKey": "dsfasdfjlkasdkfjçlasdfa"
        },
        {
            "message": "whenIsATelNumber",
            "pixKey": "(62) 98177-6411"
        }
    ]