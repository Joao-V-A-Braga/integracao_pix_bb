from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock

from rest_framework import status

class BankViewTestCase(TestCase):
    def testStatusCodeOnIndexAction(self):

        # Quando se faz um Get para a url "banks_index"
        response = self.client.get(reverse('banks_index'))
        message = "whenMethodIsGet"

        self.assertEqual(response.status_code, status.HTTP_200_OK, message)
    
        # Quando se faz um Post para a url "banks_index"
        response = self.client.post(reverse('banks_index'))
        message = "whenMethodIsPost"

        self.assertNotEqual(
            response.status_code,
            status.HTTP_200_OK,
            message
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            message
            )

    @patch('financial.models.Bank.Bank.objects.all')
    def testContentOnIndexAction(self, mock_bank):
        for data in self.dataProviderContentToIndexAction:
            mock_bank().order_by.return_value = data["content"]

            response = self.client.get(reverse('banks_index'), {'page': 1})
            mock_bank.assert_called()
            
            results = response.data.get("results", [])
            lengthOfResults = len(results)
            count = response.data.get("count", [])

            self.assertEqual(data["expectedQtt"], count)
            self.assertLessEqual(lengthOfResults, 10)

            self.assertIn("name", results[0])
            self.assertIn("code", results[0])

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoBanks",
            "content": [
                {"name":None, "code":None},
                {"name":"Banco B", "code":"002"}
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenBanks",
            "content": [
                {"name": f"Banco {i}", "code": f"{i:03d}"}
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenBanks",
            "content": [
                {"name": f"Banco {i}", "code": f"{i:03d}"}
                for i in range(1, 25)
            ],
            "expectedQtt": 24
        }
    ]
    
    