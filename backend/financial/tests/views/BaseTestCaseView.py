from django.test import TestCase
from django.urls import reverse
from unittest.mock import MagicMock

from rest_framework import status


class BaseTestCaseView(TestCase):

    # Utils -----------------------------------------------
    def assertsResponseByMethodAndRouteName(
        self, 
        status_expected:str, 
        method:str, 
        route_name:str,
        content_request:object=None,
        response_expected:object=None,
        debug=None,
        path_attr:object=None,
        content_type:str="application/json"
        ):

        other = "post"
        if method == "post":
            other = "get"
        
        # Quando se faz a requisição com o metodo e se espera o status passado
        method_function = getattr(self.client, method.lower())
        response = method_function(
            reverse(route_name, kwargs=path_attr), content_request, content_type=content_type
            ) if content_type else method_function(
            reverse(route_name, kwargs=path_attr), content_request
            )
        
        requestInfoMessage = f"| Method: {method.capitalize()} | Content: {content_request} | Response: {response.data}"
        message = f"whenMethodIs {requestInfoMessage}"
        
        # Status esperado
        self.assertEqual(response.status_code, status_expected, message)
        # Resposta esperada
        if(response_expected):
            self.assertEqual(
                response.data, response_expected, 
                f"This response is not expected {requestInfoMessage}"
                )
        
        # Quando se faz a requisição com outro metodo e se espera o status 405
        method_function = getattr(self.client, other.lower())

        response = method_function(
            reverse(route_name, kwargs=path_attr), content_request, content_type=content_type
            ) if content_type else method_function(
            reverse(route_name, kwargs=path_attr), content_request
            )
        message = f"whenMethodIsOther"
        
        self.assertNotEqual( #Não se espera o mesmo status
            response.status_code,
            status_expected,
            message
            )
        self.assertEqual( #Espera HTTP_405_METHOD_NOT_ALLOWED
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            message
            )
        
    def assertIsValidAndSaveIsCalledByMethodAndRouteName(
        self, mock_form_is_valid:MagicMock, mock_form_save:MagicMock, 
        method:str, r_name:str 
    ):
        #Define o método
        method_function = getattr(self.client, method.lower())
        
        #Quando is_valid é True se espera que chame o método save
        mock_form_is_valid.return_value = True
        method_function(reverse(r_name))

        mock_form_is_valid.assert_called_once()
        mock_form_save.assert_called_once()
        
        # Reseta os mocks para o segundo teste
        mock_form_is_valid.reset_mock()
        mock_form_save.reset_mock()

        # Envia a requisição com valid False
        mock_form_is_valid.return_value = False
        method_function(reverse(r_name))
        
        #Quando is_valid é Falso não espera que se chame o método save
        mock_form_is_valid.assert_called_once()
        mock_form_save.assert_not_called()
        
    def assertContentOnIndexAction(
        self, mock_objects_all:MagicMock, route:str, dataProvider:list[object], 
        expectedAttrInResponse:list[str]
        ):
        for data in dataProvider:
            mock_objects_all().order_by.return_value = data["content"]

            response = self.client.get(reverse(route), {'page': 1})
            mock_objects_all.assert_called()
            
            if (response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR):
                print(f"\n\n{response.data}\n\n")

            results = response.data.get("results", [])
            
            lengthOfResults = len(results)
            count = response.data.get("count", [])

            self.assertEqual(
                data["expectedQtt"], count,
                f"This quantity of elements is unexpected - {data['message']} \n\n{response.data}")
            self.assertLessEqual(lengthOfResults, 10)

            for attr in expectedAttrInResponse:
                self.assertIn(attr, results[0])
                
    def assertContentOnFindAction(
        self, mock_objects_get:MagicMock, route:str, dataProvider:list[object], 
        expectedAttrInResponse:list[str], path_attr:object=None
        ):
        for data in dataProvider:
            mock_objects_get.return_value = data["content"]

            response = self.client.get(reverse(route, kwargs=path_attr))
            mock_objects_get.assert_called()
            
            if (response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR):
                print(f"\n\n{response}\n\n")

            result = response.data

            for attr in expectedAttrInResponse:
                self.assertIn(attr, result, data['message'])