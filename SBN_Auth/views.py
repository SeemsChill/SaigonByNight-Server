# Import os.
import os
import environ
# Import built-in django.
from django.core.mail import send_mail
# Import models.
from SBN_User.models import UserInfo
# Import AUTh modules.
from django.http import response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Import REST framework.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
# Import plugins.
from SBN_User.plugins.response_plugin import handcraft_res
from .plugins.auth_plugins import generate_pseudo_csrf, verify_pseudo_csrf, generate_pseudo_email_verification_reset, verify_pseudo_email_verification

# Config the .env
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class SBN_Auth_API_GET_CSRF_Token(APIView):
    def get(self, request, format=None):
        response = Response({"message": "retrieved token successfully!"})
        response["X-CSRFToken"] = generate_pseudo_csrf() 
        return response


class SBN_Auth_API_POST_Reset(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        if verify_pseudo_csrf(request.data["csrf"]) == True:
            if UserInfo.objects.filter(email=request.data["email"]).exists():
                    credential = UserInfo.objects.get(email=request.data["email"]).platform
                    if str(credential) == "password":
                        token = generate_pseudo_email_verification_reset(request.data["isChecked"])
                        send_mail('Reset email', 'Click here: {}/verify/reset/{}'.format(env("CLIENT_SERVER_HOST"), token), 'quangkhatran1508@outlook.com.vn', [request.data["email"]], fail_silently=False)
                        return handcraft_res(201, { "email": "Email has been sent to check verification."})
                    else:
                        return handcraft_res(202, "Wrong credential.")
            return handcraft_res(404, "User not found!")
        else:
            return handcraft_res(401, "Invalid csrf token.")


class SBN_Auth_API_POST_Reset_Verification(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, *args, **kwargs):
        print(request.headers)
        """
        code, password = verify_pseudo_email_verification(request.data["code"])
        if code == 403:
            return handcraft_res(403, "Token has expired.")
        if code == 202:
            if password:
                return handcraft_res(202, { "password": password })
            else:
                return handcraft_res(202, "Reset password verified.")
        """
        return handcraft_res(202, "Accepted")
