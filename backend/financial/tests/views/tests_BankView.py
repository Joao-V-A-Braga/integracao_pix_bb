from .BaseTestCaseView import BaseTestCaseView
from django.urls import reverse
from unittest.mock import patch, MagicMock

from rest_framework import status

class BankViewTestCase(BaseTestCaseView):

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):

        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get', 
            route_name='banks_index'
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

    # Create -----------------------------------------------
    def testStatusCodeOnCreateAction(self):
        for data in self.dataProviderStatusCodeOnCreateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='post', 
                route_name='banks_create',
                content_request=data["content_request"],
                response_expected=data["response_expected"]
            )

    dataProviderStatusCodeOnCreateAction = [
        {
            "status_expected":status.HTTP_201_CREATED, 
            "content_request":{'name': 'Banco Teste', 'code': '001'},
            "response_expected":None
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{'name': 'Banco Teste'},
            "response_expected": {'code': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{'code': '987'},
            "response_expected": {'name': ['This field is required.']}
        }
    ]
    
    @patch('financial.forms.BankForm.BankForm.is_valid')
    @patch('financial.forms.BankForm.BankForm.save') 
    def testAssertCalledBankCreate(
        self, mock_form_save:MagicMock, mock_form_is_valid:MagicMock
        ):
        
        #Quando is_valid é True se espera que chame o método save
        mock_form_is_valid.return_value = True
        self.client.post(reverse('banks_create'))

        mock_form_is_valid.assert_called_once()
        mock_form_save.assert_called_once()
        
        # Reseta os mocks para o segundo teste
        mock_form_is_valid.reset_mock()
        mock_form_save.reset_mock()

        # Envia a requisição com valid False
        mock_form_is_valid.return_value = False
        self.client.post(reverse('banks_create'))
        
        #Quando is_valid é Falso não espera que se chame o método save
        mock_form_is_valid.assert_called_once()
        mock_form_save.assert_not_called()