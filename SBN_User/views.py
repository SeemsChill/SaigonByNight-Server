# Import AUTh modules.
from django.http import response
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Import REST framework.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
# Import models.
from .models import UserAuth, UserInfo, UserPlatform
# Import plugins.
from .plugins.data_plugins import register_package
from .plugins.response_plugin import handcraft_res
# Import system.
import os
# Import Firebase.
from firebase_admin import auth, credentials, initialize_app
# Import modules from other app.
from SBN_Auth.plugins.auth_plugins import generate_jwt, verify_jwt

# Get the file path.
root_dir = os.path.dirname(__file__)
app_dir = os.path.join(root_dir, "Firebase")
key_file = os.path.join(app_dir, "firebase-key.json")

app = credentials.Certificate(key_file)
initialize_app(app)

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class SBN_User_API_GET_Routes(APIView):  # get dashboard api middleware.
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        try:
            api_routes = {
                "Register (create)": "api/post/register/create/user/",
                "Register (update)": "api/post/register/update/user/",
                "Delete": "api/delete/user/"
            }
            return handcraft_res(
                200,
                api_routes
            )
        except Exception as error:
            return handcraft_res(
                400,
                error
            )


@method_decorator(csrf_protect, name="dispatch")
# post register/create user.
class SBN_User_API_POST_Register_Create_User(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        de_bundle = auth.verify_id_token(
            request.COOKIES.get("sbn-session-id"))
        bundle = {}
        bundle["uid"] = de_bundle["uid"]
        bundle["username"] = request.data["username"]
        bundle["email"] = de_bundle["email"]
        bundle["password"] = request.data["password"]
        bundle["platform"] = de_bundle["firebase"]["sign_in_provider"]
        bundle["exp"] = de_bundle["exp"]
        try:
            get_platform, package = register_package(bundle)
            platform = UserPlatform.objects.get(pk=get_platform)
            UserInfo(
                uid=package["uid"],
                username=package["username"],
                email=package["email"],
                platform=platform,
            ).save()
            if get_platform == 1:
                uid = UserInfo.objects.get(
                    uid=package["uid"]
                )
                UserAuth(
                    uid=uid,
                    username=package["username"],
                    email=package["email"],
                    password=package["password"],
                ).save()
            token = generate_jwt(package)
            return handcraft_res(201, {"success": "{} has been created!".format(package["username"]), "token": "{}".format(token)})
        except Exception as error:
            if UserInfo.objects.filter(uid=package["uid"]).exists():
                UserInfo.objects.filter(uid=package["uid"]).delete()
            if UserAuth.objects.filter(uid=package["uid"]).exists():
                UserAuth.objects.filter(uid=package["uid"]).exists()
            return handcraft_res(
                400,
                error
            )
        
@method_decorator(csrf_protect, name="dispatch")
# login the user.
class SBN_User_API_POST_Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        de_bundle = auth.verify_id_token(request.COOKIES.get("sbn-session-id"))
        bundle = {}
        bundle["uid"] = de_bundle["uid"]
        bundle["email"] = de_bundle["email"]
        bundle["password"] = request.data["password"]
        bundle["exp"] = de_bundle["exp"]
        try: 
            if UserInfo.objects.filter(uid=bundle["uid"]).exists() and UserAuth.objects.filter(password=bundle["password"]).exists():
                token = generate_jwt(bundle)
                username = UserInfo.objects.get(email=bundle["email"]).username
                return handcraft_res(202, { "success": "Welcome back {}".format(username), "token": "{}".format(token) })
        except Exception as error:
            return handcraft_res(401, error)



@method_decorator(csrf_protect, name="dispatch")
# update the user's info after registering.
class SBN_User_API_POST_Register_Update_User(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Verify jwt-token.
            de_bundle = verify_jwt(request.headers["Authorization"])
            # Process updating.
            if UserAuth.objects.filter(uid=de_bundle["uid"]).exists():
                type = register_package(request.data)
                if type == False:
                    return handcraft_res(
                        406,
                        "There's something wrong with your request package!"
                    )
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
        except Exception as error:
            return handcraft_res(
                401,
                error
            )


# Ideal: The next ideal about delete api.
# - When the user click on delete account button.
# the browser shows a form which request the user
# to enter the password. If password matches, delete the account.
@method_decorator(csrf_protect, name="dispatch")
class SBN_User_API_DELETE_Specific_User(APIView):
    permission_classes = [AllowAny]

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
