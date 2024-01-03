from django.test import TestCase

from ...models.Bank import Bank
from ...models.BankAccount import BankAccount
from ...models.PixAccount import PixAccount
from ...models.PixCharge import PixCharge

import time

class PixChargeTestCase(TestCase):

    def testPixChargeStrReturn(self):
        for data in self.dataProviderPixKey:
            bank = Bank(
                name=data["bankName"],
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
                key="61.015.142/0001-17",
                clientId="asfdsdafsadfas",
                secretId="hfdgsgfdsgfdsg",
                expire_time=time.gmtime()
            )
            
            pixCharge = PixCharge(
                pixAccount=pixAccount,
                key=data["pixKey"],
                value=data["value"],
                status=data["status"]
            )

            self.assertEqual(
                pixCharge.__str__(), 
                f"{data["value"] if data["value"] is not None and data["value"] >= 0.01 else 0.01} {data["status"]} {data["bankName"]} {data["pixKey"]}"
            )
    
    dataProviderPixKey = [
        {
            "message": "whenAllIsNone",
            "pixKey": None,
            "value": None,
            "status": None,
            "bankName": None
        },
        {
            "message": "whenAllIsFull",
            "pixKey": "61.015.142/0001-17",
            "value": 23.11,
            "status": 3,
            "bankName": "Banco do Brasil"
        },
        {
            "message": "whenValueIsZero",
            "pixKey": "61.015.142/0001-17",
            "value": 00,
            "status": 3,
            "bankName": "Banco do Brasil"
        }
    ]