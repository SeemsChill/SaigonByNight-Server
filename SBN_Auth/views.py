# Import AUTh modules.
from django.http import response
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
# Import REST framework.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class SBN_Auth_API_GET_CSRF_Token(APIView):  # get CSRF token middleware.
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        response = Response({"message": "retrieved token successfully!"})
        response["X-CSRFToken"] = get_token(request)
        return response