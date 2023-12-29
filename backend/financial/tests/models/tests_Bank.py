from django.test import TestCase

from ...models.Bank import Bank

class BankTestCase(TestCase):

    def testBankStrReturn(self):
        for data in self.dataProvider:
            bank = Bank(
                name=data['name'],
                code=data['code']
            )
            self.assertEqual(bank.__str__(), data['name'], msg=data['message'])

    def testGetCodeFormatedOfThreeDigits(self):
        for data in self.dataProvider:
            bank = Bank(
                name=data['name'],
                code=data['code']
            )

            self.assertEqual(bank.getCode(), str(data['code']).zfill(3), msg=data['message'])
    
    dataProvider = [
        {
            "message": "whenNameIsString",
            "name": "Banco do Brasil",
            "code": "001"
        },
        {
            "message": "whenNameIsNone",
            "name": None,
            "code": "001"
        },
        {
            "message": "whenNameIsNumber",
            "name": 1234,
            "code": "001"
        },
        {
            "message": "whenCodeHasLassThenThreeDigits",
            "name": "Banco do Brasil",
            "code": "01"
        }
    ]