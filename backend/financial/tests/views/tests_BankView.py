from .BaseTestCaseView import BaseTestCaseView
from django.urls import reverse
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.Bank import Bank

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
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_form_is_valid, mock_form_save=mock_form_save, 
            method="post", r_name="banks_create"
        )
    
    # Update -----------------------------------------------
    @patch('financial.forms.BankForm.BankForm.save')
    @patch('financial.models.Bank.Bank.objects.get')
    def testStatusCodeOnUpdateAction(self, mock_get:MagicMock, mock_save:MagicMock):
        mock_get.side_effect = self.fake_bank_object_get
        for data in self.dataProviderStatusCodeOnUpdateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='put',
                route_name='banks_update',
                content_request=data["content_request"],
            )

    def fake_bank_object_get(*args, **kwargs):
        if kwargs.get("id"):
            return Bank(id=kwargs.get("id"), code='001', name='Bank Name')
        else: raise Bank.DoesNotExist

    dataProviderStatusCodeOnUpdateAction = [
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 1, 'code': '001'},
        },
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 234, 'name': 'Bank Name'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'name': 'Banco Teste'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'code': '987'},
        }
    ]

    @patch('financial.models.Bank.Bank.objects.get')
    @patch('financial.forms.BankForm.BankForm.is_valid')
    @patch('financial.forms.BankForm.BankForm.save')
    def testAssertCalledBankUpdate(
        self, mock_save:MagicMock, mock_is_valid:MagicMock, mock_get:MagicMock):
        mock_get.return_value = Bank(id=1, code='001', name='Bank Name')
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_is_valid, mock_form_save=mock_save, 
            method="put", r_name="banks_update"
        )
        
        # Reseta os mocks para o segundo teste
        mock_save.reset_mock()
        mock_is_valid.reset_mock()
        mock_get.reset_mock()
        
        # Se get não tiver um id não chama save nem is_valid
        mock_get.side_effect = self.fake_bank_object_get
        self.client.put(
            reverse('banks_update'), {'name': 'Banco Teste', 'code': '987'}
            )
        
        mock_is_valid.assert_not_called()
        mock_save.assert_not_called()
        
    # Delete -----------------------------------------------
    @patch('financial.models.Bank.Bank.objects.get')
    def testStatusCodeOnDeleteAction(self, mock_get:MagicMock):
        mock_get.side_effect = self.fake_bank_object_get
        for data in self.dataProviderStatusCodeOnDeleteAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='delete',
                route_name='banks_delete',
                content_request=data["content_request"],
            )
            
    dataProviderStatusCodeOnDeleteAction = [
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 1},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{},
        }
    ]
    
    @patch('financial.models.Bank.Bank.objects.get')
    @patch('financial.models.Bank.Bank.delete')
    def testAssertCalledBankDelete(
        self, mock_delete:MagicMock, mock_get:MagicMock
        ):
        mock_get.side_effect = self.fake_bank_object_get
        self.client.delete(
            reverse('banks_delete'), {'id': 1}, content_type='application/json'
            )
        mock_delete.assert_called_once()