
# Import REST framework.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
# Import models.
from .models import UserAuth, UserInfo, UserPlatform
# Import plugins.
from .plugins.data_plugins import register_package
from .plugins.response_plugin import handcraft_res
# Import system.
import os
import environ
# Import Firebase.
from firebase_admin import auth, credentials, initialize_app
# Import modules from other app.
from SBN_Auth.plugins.auth_plugins import generate_jwt, verify_jwt, verify_pseudo_csrf

root_dir = os.path.dirname(__file__)
app_dir = os.path.join(root_dir, "Firebase")
key_file = os.path.join(app_dir, "firebase-key.json")
app = credentials.Certificate(key_file)
initialize_app(app)

# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class SBN_User_API_POST_Register_Create_User(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request, *args, **kwargs):
        try:
            emergency_uid = request.data["uid"]
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
                return handcraft_res(201, str(token))
            else:
                auth.delete_user(bundle["uid"])
                return handcraft_res(401, "Invalid csrf token!")
        except Exception as error:
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
            emergency_uid = request.data["uid"]
            de_bundle = auth.verify_id_token(request.data["sbnSessionId"])
            bundle = {}
            bundle["uid"] = de_bundle["uid"]
            bundle["email"] = de_bundle["email"]
            bundle["username"] = de_bundle["name"]
            bundle["platform"] = de_bundle["firebase"]["sign_in_provider"]
            bundle["exp"] = de_bundle["exp"]  
            if verify_pseudo_csrf(request.data["csrf"]) == True:
                if UserInfo.objects.filter(uid=bundle["uid"]).exists():
                    token = generate_jwt(bundle)
                    return handcraft_res(202, str(token))
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
                    return handcraft_res(202, str(token))
            else:
                if UserInfo.objects.filter(uid=bundle["uid"]).exists():
                    return handcraft_res(401, "Invalid csrf token.")
                else:
                    auth.delete_user(bundle["uid"])
                    return handcraft_res(401, "Invalid csrf token.")
        except Exception as error:
            if UserInfo.objects.filter(uid=emergency_uid).exists():
                return handcraft_res(401, "Error requesting to firebase")
            else:
                auth.delete_user(emergency_uid)
                return handcraft_res(400, "Bad request due to decrypting firebase token too soon.") 

class SBN_User_API_POST_Register_Update_User(APIView):
    def post(self, request, *args, **kwargs):
        de_bundle = verify_jwt(request.headers["Authorization"])
        if UserAuth.objects.filter(uid=de_bundle["uid"]).exists():
            type = register_package(request.data)
            if type == False:
                return handcraft_res(406, "There's something wrong with your request package!")
            else:
                try:
                    if UserInfo.objects.filter(uid=de_bundle["uid"]).exists():
                        UserInfo.objects.filter(uid=de_bundle["uid"]).update(
                            full_name=request.data["full_name"],
                            first_dest=request.data["first_dest"],
                            second_dest=request.data["second_dest"],
                            third_dest=request.data["third_dest"],
                            detail_adr=request.data["detail_adr"],
                            phone_number=request.data["phone_number"],
                        )
                    if UserAuth.objects.filter(uid=de_bundle["uid"]).exists():
                        UserAuth.objects.filter(uid=de_bundle["uid"]).update(is_updated=True)
                    return handcraft_res(
                        202,
                        "Update {}".format(de_bundle["uid"])
                    )
                except Exception as error:
                    return handcraft_res(
                        401,
                        error
                    )


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
