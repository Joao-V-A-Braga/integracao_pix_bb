from .BaseTestCaseView import BaseTestCaseView
from django.urls import reverse
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.BankAccount import BankAccount
from ...models.Bank import Bank

class BankAccountViewTestCase(BaseTestCaseView):
    
    def setUp(self):
        Bank.objects.create(id=1, name='Banco A', code='002')

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get', 
            route_name='bank_accounts_index'
        )

    @patch('financial.models.BankAccount.BankAccount.objects.all')
    def testContentOnIndexAction(self, mock_bank_account:MagicMock):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_bank_account, route='bank_accounts_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=["number", "agency", "cnpj", "bank"]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoBankAccounts",
            "content": [
                {
                    "number":None, "agency":None, 
                    'cnpj':None, 'bank': Bank(id=1, name='Banco A', code='002')
                },
                {
                    "number":'12431234', "agency":'342234', 
                    'cnpj':'61.015.142/0001-17', 
                    'bank': Bank(id=1, name='Banco A', code='002')
                }
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenBankAccounts",
            "content": [
                {
                    "number":f'124312{i}', "agency":f'3422{i}', 
                    'cnpj':f'61.015.142/0001-{str(i).zfill(2)}', 
                    'bank': Bank(id=i, name=f'Banco {i}', code=f'{str(i).zfill(3)}')
                }
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenBankAccounts",
            "content": [
                {
                    "number":f'124312{i}', "agency":f'3422{i}', 
                    'cnpj':f'61.015.142/0001-{str(i).zfill(2)}', 
                    'bank': Bank(id=i, name=f'Banco {i}', code=f'{str(i).zfill(3)}')
                }
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
                route_name='bank_accounts_create',
                content_request=data["content_request"],
                response_expected=data["response_expected"]
            )

    dataProviderStatusCodeOnCreateAction = [
        {
            "status_expected":status.HTTP_201_CREATED, 
            "content_request":{
                    "number":'12431234', "agency":'342234', 
                    'cnpj':'61.015.142/0001-17', 
                    'bank': 1
                },
            "response_expected":None
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "number":'12431234', "agency":'342234', 
                    'cnpj':'61.015.142/0001-17'
                },
            "response_expected": {'bank': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "number":'12431234', "agency":'342234', 
                    'bank': 1
                },
            "response_expected": {'cnpj': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "number":'12431234', 'cnpj':'61.015.142/0001-17', 
                    'bank': 1
                },
            "response_expected": {'agency': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    'agency':'342234', 'cnpj':'61.015.142/0001-17', 
                    'bank': 1
                },
            "response_expected": {'number': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "number":'12431234', "agency":'342234', 
                    'cnpj':'61.015.142/0001-17', 
                    'bank': 2
                },
            "response_expected":{
                "bank": [
                    "Select a valid choice. That choice is not one of the available choices."
                ]
            }
        },
    ]
    
    @patch('financial.forms.BankAccountForm.BankAccountForm.is_valid')
    @patch('financial.forms.BankAccountForm.BankAccountForm.save')
    def testAssertCalledBankAccountCreate(
        self, mock_form_save:MagicMock, mock_form_is_valid:MagicMock
        ):
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_form_is_valid, mock_form_save=mock_form_save, 
            method="post", r_name="bank_accounts_create"
        )
    
    # Update -----------------------------------------------
    @patch('financial.forms.BankAccountForm.BankAccountForm.save')
    @patch('financial.models.BankAccount.BankAccount.objects.get')
    def testStatusCodeOnUpdateAction(self, mock_get:MagicMock, mock_save:MagicMock):
        mock_get.side_effect = self.fake_bank_account_object_get
        for data in self.dataProviderStatusCodeOnUpdateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='put',
                route_name='bank_accounts_update',
                content_request=data["content_request"],
            )

    def fake_bank_account_object_get(*args, **kwargs):
        if kwargs.get("id"):
            return BankAccount(
                id=kwargs.get("id"), number='12431234', agency='342234',
                cnpj='61.015.142/0001-17', 
                bank=Bank(id=1, name='Banco A', code="001")
                )
        else: raise BankAccount.DoesNotExist("BankAccount matching the query does not exist.")

    dataProviderStatusCodeOnUpdateAction = [
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 1, 'number': '12431234'},
        },
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 234, 'agency': '342234'},
        },
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 543, 'cnpj': '61.015.142/0001-17'},
        },
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 1, 'bank': 1},
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{'id': 1, 'bank': 2},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'cnpj': '61.015.142/0001-17'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'agency': '342234'},
        }
    ]

    @patch('financial.models.BankAccount.BankAccount.objects.get')
    @patch('financial.forms.BankAccountForm.BankAccountForm.is_valid')
    @patch('financial.forms.BankAccountForm.BankAccountForm.save')
    def testAssertCalledBankAccountUpdate(
        self, mock_save:MagicMock, mock_is_valid:MagicMock, mock_get:MagicMock):
        mock_get.return_value = BankAccount(
                id=1, number='12431234', agency='342234',
                cnpj='61.015.142/0001-17', 
                bank=Bank(id=1, name='Banco A', code="001")
                )
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_is_valid, mock_form_save=mock_save, 
            method="put", r_name="bank_accounts_update"
        )
        
        # Reseta os mocks para o segundo teste
        mock_save.reset_mock()
        mock_is_valid.reset_mock()
        mock_get.reset_mock()
        
        # Se get não tiver um id não chama save nem is_valid
        mock_get.side_effect = self.fake_bank_account_object_get
        self.client.put(
            reverse('bank_accounts_update'), {
                    "number":'12431234', "agency":'342234', 
                    'cnpj':'61.015.142/0001-17', 
                    'bank': 1
                }
            )
        
        mock_is_valid.assert_not_called()
        mock_save.assert_not_called()
        
    # Delete -----------------------------------------------
    @patch('financial.models.BankAccount.BankAccount.objects.get')
    def testStatusCodeOnDeleteAction(self, mock_get:MagicMock):
        mock_get.side_effect = self.fake_bank_account_object_get
        for data in self.dataProviderStatusCodeOnDeleteAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='delete',
                route_name='bank_accounts_delete',
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
    
    @patch('financial.models.BankAccount.BankAccount.objects.get')
    @patch('financial.models.BankAccount.BankAccount.delete')
    def testAssertCalledBankAccountDelete(
        self, mock_delete:MagicMock, mock_get:MagicMock
        ):
        mock_get.side_effect = self.fake_bank_account_object_get
        self.client.delete(
            reverse('bank_accounts_delete'), {'id': 1}, content_type='application/json'
            )
        mock_delete.assert_called_once()