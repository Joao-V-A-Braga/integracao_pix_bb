from financial.tests.views.BaseTestCaseView import BaseTestCaseView
from django.urls import reverse
from unittest.mock import patch, MagicMock
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from rest_framework import status

from ...models.Product import Product

class ProductViewTestCase(BaseTestCaseView):

    # Index -----------------------------------------------
    def testStatusCodeOnIndexAction(self):
        self.assertsResponseByMethodAndRouteName(
            status_expected=status.HTTP_200_OK, 
            method='get',
            route_name='products_index'
        )

    @patch('sale.models.Product.Product.objects.all')
    def testContentOnIndexAction(self, mock_product):
        self.assertContentOnIndexAction(
            mock_objects_all=mock_product, route='products_index',
            dataProvider=self.dataProviderContentToIndexAction,
            expectedAttrInResponse=[
                "name", "value", "imagePath"
                ]
            )

    dataProviderContentToIndexAction = [
        {
            "message": "whenDataIsTwoProducts",
            "content": [
                {"name":"Produto A", "value":9.99, "imagePath": None},
                {"name":"Produto B", "value":29.99, "imagePath": "assets/imagem.png"}
            ],
            "expectedQtt": 2
        },
        {
            "message": "whenDataIsMoreThanTenProducts",
            "content": [
                {"name":f"Produto {i}", "value":29.99+i, "imagePath": f"assets/imagem{i}.png"}
                for i in range(1, 14)
            ],
            "expectedQtt": 13
        },
        {
            "message": "whenDataIsMoreThanTenProducts",
            "content": [
                {"name":f"Produto {i}", "value":29.99+i, "imagePath": f"assets/imagem{i}.png"}
                for i in range(1, 25)
            ],
            "expectedQtt": 24
        }
    ]

    # Create -----------------------------------------------
    @patch('sale.forms.ProductForm.ProductForm.save')
    def testStatusCodeOnCreateAction(self, mock_save):
        for data in self.dataProviderStatusCodeOnCreateAction:
            files = {'imagePath': self.getImageTest()}
            
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"],
                method='post',
                route_name='products_create',
                content_request={**data["content_request"], **files},
                response_expected=data["response_expected"],
                content_type=None
            )
            
    dataProviderStatusCodeOnCreateAction = [
        {
            "status_expected":status.HTTP_201_CREATED, 
            "content_request":{
                "name":"Produto A", "value":29.99
                },
            "response_expected":None
        },
        {
            "status_expected":status.HTTP_201_CREATED, 
            "content_request":{
                "name":"Produto B", "value":29.99
            },
            "response_expected": None
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                "name":"Produto C"
                },
            "response_expected": {'value': ['This field is required.']}
        },
        {
            "status_expected":status.HTTP_400_BAD_REQUEST, 
            "content_request":{
                "value":29.99
                },
            "response_expected": {'name': ['This field is required.']}
        }
    ]
    
    @patch('sale.forms.ProductForm.ProductForm.is_valid')
    @patch('sale.forms.ProductForm.ProductForm.save')
    def testAssertCalledBankCreate(
        self, mock_form_save:MagicMock, mock_form_is_valid:MagicMock
        ):
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_form_is_valid, mock_form_save=mock_form_save, 
            method="post", r_name="products_create"
        )
    
    # Update -----------------------------------------------
    @patch('sale.forms.ProductForm.ProductForm.save')
    @patch('sale.models.Product.Product.objects.get')
    def testStatusCodeOnUpdateAction(self, mock_get:MagicMock, mock_save:MagicMock):
        mock_get.side_effect = self.fake_product_object_get
        for data in self.dataProviderStatusCodeOnUpdateAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='put',
                route_name='products_update',
                content_request=data["content_request"]
            )

    def fake_product_object_get(*args, **kwargs):
        if kwargs.get("id"):
            return Product(id=kwargs.get("id"), value=29.99, name='Produto A', imagePath=ProductViewTestCase.getImageTest())
        else: raise Product.DoesNotExist
    
    @staticmethod
    def getImageTest():
        f = BytesIO()
        image = Image.new("RGB", (200, 200))
        image.save(f, 'jpeg')
        f.seek(0)
        
        return SimpleUploadedFile(name='test_image.jpeg', content=f.getvalue(), content_type='image/jpeg')

    dataProviderStatusCodeOnUpdateAction = [
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 1, "value":29.99},
        },
        {
            "status_expected":status.HTTP_200_OK, 
            "content_request":{'id': 234, 'name': 'Produto A'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{'name': 'Produto A'},
        },
        {
            "status_expected":status.HTTP_404_NOT_FOUND, 
            "content_request":{"value":29.99},
        }
    ]

    @patch('sale.models.Product.Product.objects.get')
    @patch('sale.forms.ProductForm.ProductForm.is_valid')
    @patch('sale.forms.ProductForm.ProductForm.save')
    def testAssertCalledBankUpdate(
        self, mock_save:MagicMock, mock_is_valid:MagicMock, mock_get:MagicMock):
        mock_get.return_value = Product(id=1, value=29.99, name='Produto A', imagePath=ProductViewTestCase.getImageTest())
        self.assertIsValidAndSaveIsCalledByMethodAndRouteName(
            mock_form_is_valid=mock_is_valid, mock_form_save=mock_save, 
            method="put", r_name="products_update"
        )
        
        # Reseta os mocks para o segundo teste
        mock_save.reset_mock()
        mock_is_valid.reset_mock()
        mock_get.reset_mock()
        
        # Se get não tiver um id não chama save nem is_valid
        mock_get.side_effect = self.fake_product_object_get
        self.client.put(
            reverse('products_update'), {'name': 'Produto A', 'imagePath': ProductViewTestCase.getImageTest()}
            )
        
        mock_is_valid.assert_not_called()
        mock_save.assert_not_called()
        
    # Delete -----------------------------------------------
    @patch('sale.models.Product.Product.objects.get')
    def testStatusCodeOnDeleteAction(self, mock_get:MagicMock):
        mock_get.side_effect = self.fake_product_object_get
        for data in self.dataProviderStatusCodeOnDeleteAction:
            self.assertsResponseByMethodAndRouteName(
                status_expected=data["status_expected"], 
                method='delete',
                route_name='products_delete',
                content_request=data["content_request"]
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
    
    @patch('sale.models.Product.Product.objects.get')
    @patch('sale.models.Product.Product.delete')
    def testAssertCalledProductDelete(
        self, mock_delete:MagicMock, mock_get:MagicMock
        ):
        mock_get.side_effect = self.fake_product_object_get
        self.client.delete(
            reverse('products_delete'), {'id': 1}, content_type='application/json'
            )
        mock_delete.assert_called_once()