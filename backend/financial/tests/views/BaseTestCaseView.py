from django.test import TestCase
from django.urls import reverse

from rest_framework import status


class BaseTestCaseView(TestCase):

    # Utils -----------------------------------------------
    def assertsResponseByMethodAndRouteName(
        self, 
        status_expected:str, 
        method:str, 
        route_name:str,
        content_request:object=None,
        response_expected:object=None
        ):

        other = "post"
        if method == "post":
            other = "get"
        
        # Quando se faz a requisição com o metodo e se espera o status passado
        method_function = getattr(self.client, method.lower())
        response = method_function(reverse(route_name), content_request)
        
        message = f"whenMethodIs{method.capitalize()}"
        
        # Status esperado
        self.assertEqual(response.status_code, status_expected, message)
        # Resposta esperada
        if(response_expected):
            self.assertEqual(response.data, response_expected, "This response is not expected")
        
        # Quando se faz a requisição com outro metodo e se espera o status 405
        method_function = getattr(self.client, other.lower())
        response = method_function(reverse(route_name), content_request)
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