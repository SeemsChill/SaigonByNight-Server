# utils.
import os
import environ
# rest_framework.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
# models.
from .models import Product
# plugins.
from .plugins.product_plug import list_all_products
from SBN_User.plugins.response_plugin import handcraft_res
from SBN_Auth.plugins.product_plugins import decrypt_authorization_jwt

# setup .env.
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# bypass built-in csrf.
class CsrfExemptSesstionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

# get entire products involve with current user.
class GetListProduct(APIView):
    def get(self, request):
        return_package = decrypt_authorization_jwt(request.headers['Authorization'])
        if str(type(return_package)) == "<class 'str'>":
            products = list_all_products(Product.objects.filter(owner_uid=return_package))
            return handcraft_res(202, products)
        else:
            return handcraft_res(401, {'message': 'Invalid or expired jwt.'})

