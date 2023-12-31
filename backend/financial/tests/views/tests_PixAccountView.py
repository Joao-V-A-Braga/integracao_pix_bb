from .BaseTestCaseView import BaseTestCaseView
from django.urls import reverse
from unittest.mock import patch, MagicMock

from rest_framework import status

from ...models.BankAccount import BankAccount
from ...models.Bank import Bank
from ...models.PixAccount import PixAccount

import time

class PixAccountViewTestCase(BaseTestCaseView):
    
    def setUp(self):
        bank = Bank.objects.create(name='Banco A', code="001")
        BankAccount.objects.create(
            id=1,
            number='12431256', agency='342256',
            cnpj='61.015.142/0001-18', 
            bank=bank
            )

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get', 
            route_name='pix_accounts_index'
        )

    @patch('financial.models.PixAccount.PixAccount.objects.all')
    def testContentOnIndexAction(self, mock_pix_account:MagicMock):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_pix_account, route='pix_accounts_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=[
                "bankAccount", "key", "clientId", "expire_time"
                ]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoPixAccounts",
            "content": [
                {
                    'bankAccount': BankAccount(
                        id=1, number='12431234', agency='342234',
                        cnpj='61.015.142/0001-17', 
                        bank=Bank(id=1, name='Banco A', code="001")
                    ),
                    "key":'61.015.142/0001-17', "clientId":"asfdsdafsadfas", 
                    'secretId':"hfdgsgfdsgfdsg", 'expire_time': 1647838478
                },
                {
                    'bankAccount': BankAccount(
                        id=1, number='12431256', agency='342256',
                        cnpj='61.015.142/0001-18', 
                        bank=Bank(id=1, name='Banco B', code="002")
                    ),
                    "key":'61.015.142/0001-56', "clientId":"asfdsdafsadfty", 
                    'secretId':"hfdgsgfdsgfcvb", 'expire_time': 1647838478
                },
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenPixAccounts",
            "content": [
                {
                    'bankAccount': BankAccount(
                        id=i, number='12431256', agency='342256',
                        cnpj=f'61.015.142/0001-{10+i}', 
                        bank=Bank(id=i, name=f'Banco {i}', code="002")
                    ),
                    "key":'61.015.142/0001-56', "clientId":f"asfds{i}afsadfty", 
                    'secretId':f"hfdgsgfdsgfcv{i}", 'expire_time': 1647838478+i
                }
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenPixAccounts",
            "content": [
                {
                    'bankAccount': BankAccount(
                        id=i, number='12431256', agency='342256',
                        cnpj=f'61.015.142/0001-{10+i}', 
                        bank=Bank(id=i, name=f'Banco {i}', code="002")
                    ),
                    "key":'61.015.142/0001-56', "clientId":f"asfds{i}afsadfty", 
                    'secretId':f"hfdgsgfdsgfcv{i}", 'expire_time': 1647838478+i
                }
                for i in range(1, 25)
            ],
            "expectedQtt": 24
        }
    ]

    # Create -----------------------------------------------
    @patch('financial.forms.PixAccountForm.PixAccountForm.save')
    def testStatusCodeOnCreateAction(self, mock_save):
        for data in self.dataProviderStatusCodeOnCreateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"],
                method='post',
                route_name='pix_accounts_create',
                content_request=data["content_request"],
                response_expected=data["response_expected"]
            )

    dataProviderStatusCodeOnCreateAction = [
        {
            "status_expected":status.HTTP_201_CREATED, 
            "content_request":{
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'expire_time': 1, 
                    'bankAccount': 1
                },
            "response_expected":None
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'bankAccount': 1
                },
            "response_expected": {'expire_time': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'expire_time': 1, 'bankAccount': 1
                },
            "response_expected": {'secretId': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "key":'61.015.142/0001-56', 'secretId':"hfdgsgfdsgfcv", 
                    'expire_time': 1, 'bankAccount': 1
                },
            "response_expected": {'clientId': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'expire_time': 1, 
                    'bankAccount': 1
                },
            "response_expected": {'key': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'expire_time': 1
                },
            "response_expected": {'bankAccount': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'expire_time': 1, 
                    'bankAccount': 2
                },
            "response_expected":{
                "bankAccount": [
                    "Select a valid choice. That choice is not one of the available choices."
                ]
            }
        }
    ]
    
    @patch('financial.forms.PixAccountForm.PixAccountForm.is_valid')
    @patch('financial.forms.PixAccountForm.PixAccountForm.save')
    def testAssertCalledPixAccountCreate(
        self, mock_form_save:MagicMock, mock_form_is_valid:MagicMock
        ):
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_form_is_valid, mock_form_save=mock_form_save, 
            method="post", r_name="pix_accounts_create"
        )
    
    # Update -----------------------------------------------
    @patch('financial.forms.PixAccountForm.PixAccountForm.save')
    @patch('financial.models.PixAccount.PixAccount.objects.get')
    def testStatusCodeOnUpdateAction(self, mock_get:MagicMock, mock_save:MagicMock):
        mock_get.side_effect = self.fake_pix_account_object_get
        for data in self.dataProviderStatusCodeOnUpdateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='put',
                route_name='pix_accounts_update',
                content_request=data["content_request"],
            )

    def fake_pix_account_object_get(*args, **kwargs):
        if kwargs.get("bankAccount"):
            return PixAccount(
                key='61.015.142/0001-56', clientId='asfdsafsadfty',
                secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                bankAccount=BankAccount(
                        id=kwargs.get("bankAccount"), number='12431234', agency='342234',
                        cnpj='61.015.142/0001-17', 
                        bank=Bank(id=1, name='Banco A', code="001")
                    )
                )
        else: return None

    dataProviderStatusCodeOnUpdateAction = [
        {
            "status_expected":status.HTTP_200_OK,
            "content_request":{'bankAccount': 1, 'key': '61.015.142/0001-55'},
        },
        {
            "status_expected":status.HTTP_200_OK,
            "content_request":{'bankAccount': 1, 'clientId': 'hfdgsgfdsgfcv'},
        },
        {
            "status_expected":status.HTTP_200_OK,
            "content_request":{'bankAccount': 1, 'secretId': 'asfdsafsadfty'},
        },
        {
            "status_expected":status.HTTP_200_OK,
            "content_request":{'bankAccount': 1, 'expire_time': 3},
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST,
            "content_request":{'bankAccount': 2, 'secretId': 'asfdsafsadfty'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'secretId': 'asfdsafsadfty'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'expire_time': 3},
        }
    ]

    @patch('financial.models.PixAccount.PixAccount.objects.get')
    @patch('financial.forms.PixAccountForm.PixAccountForm.is_valid')
    @patch('financial.forms.PixAccountForm.PixAccountForm.save')
    def testAssertCalledPixAccountUpdate(
        self, mock_save:MagicMock, mock_is_valid:MagicMock, mock_get:MagicMock):
        mock_get.return_value = PixAccount(
                key='61.015.142/0001-56', clientId='asfdsafsadfty',
                secretId='hfdgsgfdsgfcv', expire_time=1647838478,
                bankAccount=BankAccount(
                        id=1, number='12431234', agency='342234',
                        cnpj='61.015.142/0001-17', 
                        bank=Bank(id=1, name='Banco A', code="001")
                    )
                )
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_is_valid, mock_form_save=mock_save, 
            method="put", r_name="pix_accounts_update"
        )
        
        # Reseta os mocks para o segundo teste
        mock_save.reset_mock()
        mock_is_valid.reset_mock()
        mock_get.reset_mock()
        
        # Se get não tiver um id não chama save nem is_valid
        mock_get.side_effect = self.fake_pix_account_object_get
        self.client.put(
            reverse('pix_accounts_update'), {
                    "key":'61.015.142/0001-56', "clientId":"asfdsafsadfty", 
                    'secretId':"hfdgsgfdsgfcv", 'expire_time': 1, 
                    'bankAccount': 1
                }
            )
        
        mock_is_valid.assert_not_called()
        mock_save.assert_not_called()
        
    # Delete -----------------------------------------------
    @patch('financial.models.PixAccount.PixAccount.objects.get')
    def testStatusCodeOnDeleteAction(self, mock_get:MagicMock):
        mock_get.side_effect = self.fake_pix_account_object_get
        for data in self.dataProviderStatusCodeOnDeleteAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='delete',
                route_name='pix_accounts_delete',
                content_request=data["content_request"],
            )
            
    dataProviderStatusCodeOnDeleteAction = [
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'bankAccount': 1},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{},
        }
    ]
    
    @patch('financial.models.PixAccount.PixAccount.objects.get')
    @patch('financial.models.PixAccount.PixAccount.delete')
    def testAssertCalledPixAccountDelete(
        self, mock_delete:MagicMock, mock_get:MagicMock
        ):
        mock_get.side_effect = self.fake_pix_account_object_get
        self.client.delete(
            reverse('pix_accounts_delete'), {'bankAccount': 1}, content_type='application/json'
            )
        mock_delete.assert_called_once()