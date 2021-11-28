# Import REST framework.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
# Import models.
from .models import UserAuth, UserInfo, UserPlatform
# Import plugins.
from .plugins.data_plugins import register_package
from .plugins.response_plugin import handcraft_res
from .plugins.user_plugin import get_user_info
# Import system.
import os
import environ
# Import Firebase.
from firebase_admin import auth, credentials, initialize_app
# Import modules from other app.
from SBN_Auth.plugins.auth_plugins import generate_jwt, generate_pseudo_email_verification_register, verify_jwt, verify_pseudo_csrf, verify_pseudo_email_verification_register
#Import built-in django.
from django.core.mail import send_mail

# For firebase.
root_dir = os.path.dirname(__file__)
app_dir = os.path.join(root_dir, "Firebase")
key_file = os.path.join(app_dir, "firebase-key.json")
app = credentials.Certificate(key_file)
initialize_app(app)

# For env.
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class SBN_User_API_POST_Register_Create_User(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        try:
            de_bundle = auth.verify_id_token(request.data["sbnSessionId"])
            bundle = {}
            bundle["uid"] = de_bundle["uid"]
            bundle["email"] = de_bundle["email"]
            bundle["platform"] = de_bundle["firebase"]["sign_in_provider"]
            bundle["username"] = request.data["username"]
            bundle["password"] = request.data["password"]
            bundle["exp"] = de_bundle["exp"]
            if verify_pseudo_csrf(request.data["csrf"]) == True:
                platform = UserPlatform.objects.get(pk=1)
                UserInfo(
                    uid=bundle["uid"],
                    username=bundle["username"],
                    email=bundle["email"],
                    platform=platform,
                ).save()
                uid = UserInfo.objects.get(
                    uid=bundle["uid"]
                )
                UserAuth(
                    uid=uid,
                    username=bundle["username"],
                    email=bundle["email"],
                    password=bundle["password"],
                ).save()
                token = generate_jwt(bundle)
                email_token = generate_pseudo_email_verification_register(bundle)
                print(bundle['email'])
                send_mail('Email verification', 'Click here: {}/verify/register/{}'.format(env('CLIENT_SERVER_HOST'), email_token), 'quangkhatran1508@outlook.com.vn', [bundle['email']], fail_silently=False)
                return handcraft_res(201, str(token))
            else:
                auth.delete_user(bundle["uid"])
                return handcraft_res(401, "Invalid csrf token!")
        except Exception as error:
            print(error)
            emergency_uid = request.data["uid"]
            if UserInfo.objects.filter(uid=emergency_uid).exists():
                return handcraft_res(401, "Error requesting to Firebase.")
            else:
                auth.delete_user(emergency_uid)
                return handcraft_res(400, "Bad request due to decrypting firebase token too soon.")


class SBN_User_API_POST_Login(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        try:
            de_bundle = auth.verify_id_token(request.data["sbnSessionId"])
            bundle = {}
            bundle["uid"] = de_bundle["uid"]
            bundle["email"] = de_bundle["email"]
            bundle["password"] = request.data["password"]
            bundle["exp"] = de_bundle["exp"]
            if verify_pseudo_csrf(request.data["csrf"]) == True:
                if UserInfo.objects.filter(uid=bundle["uid"]).exists() and UserAuth.objects.filter(password=bundle["password"]).exists():
                    token = generate_jwt(bundle)
                    return handcraft_res(202, token)
                return handcraft_res(404, "User not found.")
            else:
                return handcraft_res(401, "Invalid csrf token.")
        except Exception as error:
            return handcraft_res(401, "Login failed due to firebase token.")


class SBN_User_API_POST_Credential_3rd_Party(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        try:
            de_bundle = auth.verify_id_token(request.data["sbnSessionId"])
            bundle = {}
            bundle["uid"] = de_bundle["uid"]
            bundle["email"] = de_bundle["email"]
            bundle['username'] = ''
            if 'name' in de_bundle:
                bundle["username"] = de_bundle["name"]
            else:
                bundle['username'] = 'Anonymous'
            bundle["platform"] = de_bundle["firebase"]["sign_in_provider"]
            bundle["exp"] = de_bundle["exp"]
            if verify_pseudo_csrf(request.data["csrf"]) == True:
                if UserInfo.objects.filter(uid=bundle["uid"]).exists():
                    token = generate_jwt(bundle)
                    return handcraft_res(202, token)
                else:
                    pk_platform = 2 if bundle["platform"] == "google.com" else 3
                    platform = UserPlatform.objects.get(pk=pk_platform)
                    UserInfo(
                        uid=bundle["uid"],
                        email=bundle["email"],
                        username=bundle["username"],
                        platform=platform
                    ).save()
                    token = generate_jwt(bundle)
                    return handcraft_res(202, token)
            else:
                if UserInfo.objects.filter(uid=bundle["uid"]).exists():
                    return handcraft_res(401, "Invalid csrf token.")
                else:
                    auth.delete_user(bundle["uid"])
                    return handcraft_res(401, "Invalid csrf token.")
        except Exception as error:
            print(error)
            emergency_uid = request.data["uid"]
            if UserInfo.objects.filter(uid=emergency_uid).exists():
                return handcraft_res(401, "Error requesting to firebase")
            else:
                auth.delete_user(emergency_uid)
                return handcraft_res(400, "Bad request due to decrypting firebase token too soon.")


class GetUserProfile(APIView):
    def get(self, request):
        if verify_pseudo_csrf(request.headers['csrftoken']) == True:
            return_package = verify_jwt(request.headers['Authorization'])
            if str(type(return_package)) == "<class 'str'>":
                package = get_user_info(return_package)
                return handcraft_res(202, package)
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt token.'})
        else:
            return handcraft_res(401, { 'message': 'Invalid csrftoken.' })


class SBN_User_API_POST_Register_Update_User(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        if verify_pseudo_csrf(request.data["csrf"]) == True:
            return_package = verify_jwt(request.headers['Authorization'])
            if str(type(return_package)) == "<class 'str'>":
                UserInfo.objects.filter(uid=return_package).update(
                    full_name=request.data['realName'],
                    phone_number=request.data['phoneNumber'],
                    detail_adr=request.data['detailAddress']
                )
                if request.data['province']:
                    UserInfo.objects.filter(uid=return_package).update(
                        province=request.data['province'],
                    )
                if request.data['district']:
                    UserInfo.objects.filter(uid=return_package).update(
                        district=request.data['district'],
                    )
                if request.data['ward']:
                    UserInfo.objects.filter(uid=return_package).update(
                        ward=request.data['ward'],
                    )
                return handcraft_res(202, 'Update successfully.')
            else:
                return handcraft_res(401, { 'message': 'Invalid or expired jwt' })
        else:
            return handcraft_res(401, { 'message': 'Invalid csrftoken' })



# Ideal: The next ideal about delete api.
# - When the user click on delete account button.
# the browser shows a form which request the user
# to enter the password. If password matches, delete the account.
class SBN_User_API_DELETE_Specific_User(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            de_bundle = verify_jwt(request.headers["Authorization"])
            try:
                if UserInfo.objects.filter(uid=de_bundle["uid"]).exists():
                    # Ideal: get the name of the user and pass to the response.
                    UserInfo.objects.filter(uid=de_bundle["uid"]).delete()
                    return handcraft_res(
                        202,
                        "Delete"
                    )
            except Exception as error:
                return handcraft_res(
                    401,
                    error
                )
        except Exception as error:
            return handcraft_res(
                401,
                error
            )
