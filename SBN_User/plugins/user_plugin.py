from ..models import  UserInfo


def get_user_info(uid):
    username = UserInfo.objects.get(uid=uid).username
    email = UserInfo.objects.get(uid=uid).email
    real_name = UserInfo.objects.get(uid=uid).full_name
    province = UserInfo.objects.get(uid=uid).province
    district = UserInfo.objects.get(uid=uid).district
    ward = UserInfo.objects.get(uid=uid).ward
    phone_number = UserInfo.objects.get(uid=uid).phone_number
    if phone_number != '':
        phone_number = str(phone_number).split('+84')
        phone_number = phone_number[1]
    detail_address = UserInfo.objects.get(uid=uid).detail_adr

    return {
        'username': username,
        'email': email,
        'real_name': real_name,
        'province': province,
        'district': district,
        'ward': ward,
        'phone_number': str(phone_number),
        'detail_address': detail_address
    }
