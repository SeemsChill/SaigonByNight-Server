import jwt
import time
from uuid import uuid4
# For generating secure password.
import secrets
import string
# Import modules from other app.
from SBN_User.plugins.response_plugin import handcraft_res
from SBN_User.models import UserAuth, UserInfo
# Import Firebase admin.
from firebase_admin import auth

email_verification_key = 'GrhQ6LZnpOa0B2QQOuxOkmW8pYT299A3'
csrf_key = "Saigon_By_Night_CSRF"
secret_key = "Saigon_By_Night"

def generate_jwt(data):
    jwt_token = "Bearer {}".format(jwt.encode(
        {"uid": data["uid"], "exp": data["exp"]}, secret_key, algorithm="HS256"))
    return jwt_token

def verify_jwt(key):
    list = ["uid", "exp"]
    result = key.split(" ")
    try:
        decoded_key = jwt.decode(result[1], secret_key, algorithms="HS256")
        # Check format.
        for item in list:
            if item not in decoded_key:
                return handcraft_res(401, "Unauthorized jwt key token!")
        # Check the expiration date.
        current_now = int(time.time())
        if current_now > int(decoded_key["exp"]):
            return handcraft_res(403, "Token has expired {} > {}".format(current_now, decoded_key["exp"]))
        if UserAuth.objects.filter(uid=decoded_key["uid"]).exists() == False:
            return handcraft_res(403, "User not found in the database!")
        return decoded_key
    except Exception as error:
        return handcraft_res(401, error)

def generate_pseudo_csrf():
    jwt_token = "{}".format(jwt.encode({"flag": "khadeptraithanhlichvodichkhapvutru"}, csrf_key, algorithm="HS256"))
    return jwt_token

def verify_pseudo_csrf(key):
    try:
        decoded_key = jwt.decode(key, csrf_key, algorithms="HS256")
        if decoded_key["flag"] == "khadeptraithanhlichvodichkhapvutru":
            return True
        return False
    except Exception as error:
        return handcraft_res(401, error)

def generate_pseudo_email_verification_register(data):
    current_now = int(time.time()) + 3600
    jwt_token = '{}'.format(jwt.encode({'exp': current_now, 'email': data['email']}, email_verification_key, algorithm='HS256'))
    return jwt_token

def verify_pseudo_email_verification_register(key):
    try:
        decoded_key = jwt.decode(key, email_verification_key, algorithms='HS256')
        print(UserAuth.objects.get(email=decoded_key['email']).is_verified)
        if UserAuth.objects.get(email=decoded_key['email']).is_verified == True:
            return 410
        current_now = int(time.time())
        if current_now < int(decoded_key['exp']):
            obj = UserInfo.objects.get(email=decoded_key['email']).uid
            auth.update_user(
                obj,
                email_verified=True
            )
            UserAuth.objects.filter(email=decoded_key['email']).update(is_verified=True)
            return 202
        return 410
    except Exception as error:
        if str(error) == 'Signature has expired':
            return 410
        else:
            return 401


def generate_pseudo_email_verification_reset(data):
    current_now = int(time.time()) + 3600
    jwt_token = "{}".format(jwt.encode({"exp": current_now, "email": data["email"], "get_password": data["isChecked"]}, secret_key, algorithm="HS256"))
    return jwt_token


def verify_pseudo_email_verification(key):
    try:
        decoded_key = jwt.decode(key, secret_key, algorithms="HS256")
        if UserAuth.objects.get(email=decoded_key["email"]).is_reset == True:
            return 410, ''
        current_now = int(time.time())
        if current_now < int(decoded_key["exp"]):
            if decoded_key["get_password"] == True:
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(20))
                return 202, password
            return 202, ""
        return 410, ""
    except Exception as error:
        if str(error) == 'Signature has expired':
            return 410, ''
        else:
            return 401, ''

def verify_email_after_verification(key):
    try:
        decoded_key = jwt.decode(key, secret_key, algorithms='HS256')
        if UserAuth.objects.get(email=decoded_key['email']).is_reset == True:
            return 410, ''
        else:
            UserAuth.objects.filter(email=decoded_key['email']).update(is_reset=True)
            return 202, '{}'.format(decoded_key['email'])
    except Exception as error:
        return 401, ''
