# Import AUTh modules.
from django.http import response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Import REST framework.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .plugins.auth_plugins import generate_pseudo_csrf 

# Create your views here.

class SBN_Auth_API_GET_CSRF_Token(APIView):
    def get(self, request, format=None):
        response = Response({"message": "retrieved token successfully!"})
        response["X-CSRFToken"] = generate_pseudo_csrf() 
        return response
