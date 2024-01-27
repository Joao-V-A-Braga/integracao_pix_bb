from django.test import TestCase

from ...models.Product import Product

class ProductTestCase(TestCase):

    def testBankStrReturn(self):
        for data in self.dataProvider:
            product = Product(
                name=data['name'],
                value=data['value'],
                imagePath=data['imagePath']
            )
            self.assertEqual(product.__str__(), f"{data['name']} {data['value']}", msg=data['message'])
    
    dataProvider = [
        {
            "message": "whenIsFull",
            "name": "Banco do Brasil",
            "value": 199.99,
            "imagePath": "assets/pathdaimagem"
        },
    ]