# utils.
import os
import environ
from uuid import uuid4
# rest_framework.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# models.
from .models import Category, Product, Bill
from SBN_User.models import UserInfo
# plugins.
from .plugins.product_plug import list_all_products, list_product_dashboard, algorithm_location_near_you, return_bills_client, return_bills_owner
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
                    description=request.data['productDescription'],
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

# update a product.
class UpdateProduct(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if verify_pseudo_csrf(request.headers['Authorization']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if (str(type(return_package))) == "<class 'str'>":
                Product.objects.filter(prod_uid=request.data['productUid']).update(
                    name=request.data['productName'],
                    description=request.data['productDescription'],
                    quantity=request.data['productQuantity'],
                    current_quantity=request.data['productQuantity'],
                    price=request.data['productPrice']
                )
                return handcraft_res(202, { 'message': 'updated the package.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })

# delete a product.
class DeleteProduct(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if (str(type(return_package))) == "<class 'str'>":
                Product.objects.filter(prod_uid=request.data['productUid']).delete()
                return handcraft_res(202, { 'message': 'deleted the product.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })


# get all the product.
class ListAllTheProduct(APIView):
    def get(self, request):
        if 'Authorization' in request.headers:
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if(str(type(return_package))) == "<class 'str'>":
                if (UserInfo.objects.get(uid=return_package).province):
                    province = UserInfo.objects.get(uid=return_package).province
                    products = algorithm_location_near_you(return_package, province)
                    return handcraft_res(202, products)
                else:
                    products = list_product_dashboard(Product.objects.all())
                    return handcraft_res(202, products)
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.' })
            return handcraft_res(202, { 'message': 'get all product near you.' })
        else:
            products = list_product_dashboard(Product.objects.all())
            return handcraft_res(202, products)


class BuyTheProduct(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if (str(type(return_package))) == "<class 'str'>":
                owner_uid=UserInfo.objects.get(uid=request.data['ownerUid'])
                client_uid=UserInfo.objects.get(uid=request.data['clientUid'])
                product_uid=Product.objects.get(prod_uid=request.data['productUid'])
                bill_uid=uuid4().hex
                Bill(
                    bill_uid=bill_uid,
                    owner_uid=owner_uid,
                    client_uid=client_uid,
                    prod_uid=product_uid,
                    quantity=request.data['quantity'],
                ).save()
                return handcraft_res(202, { 'message': 'we bought your product.' })
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })

class GetAllBillsForClient(APIView):
    def get(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if(str(type(return_package))) == "<class 'str'>":
                if Bill.objects.filter(client_uid=return_package).exists():
                    bills = Bill.objects.filter(client_uid=return_package)
                    list_bills = return_bills_client(bills)
                    return handcraft_res(202, list_bills)
                return handcraft_res(202, { 'message': 'nothing' })
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })


class GetAllBillsForOwner(APIView):
    def get(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if(str(type(return_package))) == "<class 'str'>":
                if Bill.objects.filter(owner_uid=return_package).exists():
                    bills = Bill.objects.filter(owner_uid=return_package)
                    list_bill = return_bills_owner(bills)
                    return handcraft_res(202, list_bill)
                return handcraft_res(202, { 'message': 'nothing'})
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })


class BillAction(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']):
            return_package = decrypt_authorization_jwt(request.headers['Authorization'])
            if(str(type(return_package))) == "<class 'str'>":
                prod_uid = Bill.objects.get(bill_uid=request.data['bill_uid']).prod_uid
                quantity = Bill.objects.get(bill_uid=request.data['bill_uid']).quantity
                current_quantity = Product.objects.get(prod_uid=prod_uid).current_quantity
                quantity_cal = current_quantity - quantity
                if quantity_cal == 0 or quantity_cal < 0:
                    Product.objects.filter(prod_uid=prod_uid).delete()
                    Bill.objects.filter(bill_uid=request.data['bill_uid']).delete()
                    return handcraft_res(202, { 'message': 'delivered successfully.'})
                # update the quantity.
                Product.objects.filter(prod_uid=prod_uid).update(current_quantity=quantity_cal)
                # delete the product.
                Bill.objects.filter(bill_uid=request.data['bill_uid']).delete()
                return handcraft_res(202, { 'message': 'delivered successfully.'})
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.' })
        else:
            return handcraft_res(401, { 'message': 'Invalid or expired csrf token.' })
