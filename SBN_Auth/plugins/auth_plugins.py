import jwt
import time
from uuid import uuid4
# Import modules from other app.
from SBN_User.plugins.response_plugin import handcraft_res
from SBN_User.models import UserAuth

secret_key = "Saigon_By_Night"
csrf_key = "Saigon_By_Night_CSRF"

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

def generate_pseudo_email_verification_reset(isChecked):
    current_now = int(time.time()) + 3600
    jwt_token = "{}".format(jwt.encode({"exp": current_now, "get_password": isChecked}, secret_key, algorithm="HS256"))
    return jwt_token

def verify_pseudo_email_verification(key):
    try:
        decoded_key = jwt.decode(key, secret_key, algorithms="HS256")
        current_now = int(time.time())
        if current_now < int(decoded_key["exp"]):
            if decoded_key["get_password"] == True:
                return 202, uuid4().hex
            return 202
        return 403
    except Exception as error:
        return handcraft_res(401, error)
