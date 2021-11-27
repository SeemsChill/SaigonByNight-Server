# utils.
import os
import environ
from uuid import uuid4
# rest_framework.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# models.
from .models import Category, Product
from SBN_User.models import UserInfo
# plugins.
from .plugins.product_plug import list_all_products
from SBN_User.plugins.response_plugin import handcraft_res
from SBN_Auth.plugins.product_plugins import decrypt_authorization_jwt
from SBN_Auth.plugins.auth_plugins import verify_pseudo_csrf

# setup .env.
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# bypass built-in csrf.
class CsrfExemptSessionAuthentication(SessionAuthentication):
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


# create a product.
class CreateProduct(APIView):
    parser_classes = (MultiPartParser, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, format=None):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if (str(type(return_package))) == "<class 'str'>":
                owner_uid = UserInfo.objects.get(uid=return_package)
                # remember to change this pk.
                category = Category.objects.get(pk=1)
                Product(
                    owner_uid=owner_uid,
                    prod_uid=str(uuid4().hex),
                    name=request.data['productName'],
                    category=category,
                    image=request.FILES['productImage'],
                    quantity=int(request.data['productQuantity']),
                    current_quantity=int(request.data['productQuantity']),
                    price=request.data['productPrice'],
                    discount=0,
                ).save()
                return handcraft_res(202, { 'message': 'message accepted.' })
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })
