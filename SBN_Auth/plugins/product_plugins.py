import jwt
from SBN_User.models import UserInfo

secret_key = "PbdXdab>6+r-rZQQ"

def decrypt_authorization_jwt(key: str):
    true_key = key.split(' ')

    try:
        decrypt = jwt.decode(true_key[1], secret_key, algorithms='HS256')
        if UserInfo.objects.filter(uid=decrypt['uid']).exists():
            return decrypt['uid']
        return 401
    except:
        return 401
