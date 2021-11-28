# models.
from ..models import Product, Bill
from SBN_User.models import UserInfo
# plugins.
from .status_plug import status_calculator, status_detector

# get all products for the dashboard. (name and status)
def list_all_products(products):
    dashboard_product = {}

    for product in products:
        prod_uid = Product.objects.get(prod_uid=product).prod_uid
        name = Product.objects.get(prod_uid=product).name
        description = Product.objects.get(prod_uid=product).description
        quantity = Product.objects.get(prod_uid=product).quantity
        current_quantity = Product.objects.get(prod_uid=product).current_quantity
        price = Product.objects.get(prod_uid=product).price
        status_percentage = status_calculator(int(current_quantity), int(quantity))
        status_zone = status_detector(status_percentage)

        dashboard_product[prod_uid] = {}
        dashboard_product[prod_uid]['uid'] = prod_uid
        dashboard_product[prod_uid]['name'] = name
        dashboard_product[prod_uid]['current_quantity'] = int(current_quantity)
        dashboard_product[prod_uid]['status_zone'] = str(status_zone)
        dashboard_product[prod_uid]['description'] = str(description)
        dashboard_product[prod_uid]['price'] = int(price)

    return dashboard_product

def list_product_dashboard(products):
    list_product = {}

    for product in products:
        # get product info.
        prod_uid = Product.objects.get(prod_uid=product).prod_uid
        name = Product.objects.get(prod_uid=product).name
        description = Product.objects.get(prod_uid=product).description
        quantity = Product.objects.get(prod_uid=product).quantity
        current_quantity = Product.objects.get(prod_uid=product).current_quantity
        price = Product.objects.get(prod_uid=product).price
        status_percentage = status_calculator(int(current_quantity), int(quantity))
        status_zone = status_detector(status_percentage)

        # get owner info.
        owner_uid = Product.objects.get(prod_uid=product).owner_uid
        username = UserInfo.objects.get(uid=owner_uid).username
        province = UserInfo.objects.get(uid=owner_uid).province
        district = UserInfo.objects.get(uid=owner_uid).district
        ward = UserInfo.objects.get(uid=owner_uid).ward
        username = UserInfo.objects.get(uid=owner_uid).username
        phone_number = UserInfo.objects.get(uid=owner_uid).phone_number

        list_product[prod_uid] = {}
        list_product[prod_uid]['prod_uid'] = prod_uid
        list_product[prod_uid]['prod_name'] = name
        list_product[prod_uid]['prod_description'] = description
        list_product[prod_uid]['prod_current_quantity'] = int(current_quantity)
        list_product[prod_uid]['prod_price'] = int(price)
        list_product[prod_uid]['prod_status_zone'] = str(status_zone)
        list_product[prod_uid]['username'] = username
        list_product[prod_uid]['province'] = province
        list_product[prod_uid]['district'] = district
        list_product[prod_uid]['ward'] = ward
        list_product[prod_uid]['phone_number'] = str(phone_number)

    return list_product

data = [{ "id":294, "name":"Hồ Chí Minh" },
    {
        "id":297,
        "name":"Hà Nội"
    },
    {
    "id":291,
    "name":"Đà Nẵng"
    },
    {
    "id":278,
    "name":"An Giang"
    },
    {
    "id":280,
    "name":"Bà Rịa - Vũng Tàu"
    },
    {
    "id":282,
    "name":"Bắc Giang"
    },
    {
    "id":281,
    "name":"Bắc Kạn"
    },
    {
    "id":279,
    "name":"Bạc Liêu"
    },
    {
    "id":283,
    "name":"Bắc Ninh"
    },
    {
    "id":284,
    "name":"Bến Tre"
    },
    {
    "id":285,
    "name":"Bình Dương"
    },
    {
    "id":286,
    "name":"Bình Phước"
    },
    {
    "id":287,
    "name":"Bình Thuận"
    },
    {
    "id":316,
    "name":"Bình Định"
    },
    {
    "id":289,
    "name":"Cà Mau"
    },
    {
    "id":290,
    "name":"Cần Thơ"
    },
    {
    "id":288,
    "name":"Cao Bằng"
    },
    {
    "id":293,
    "name":"Gia Lai"
    },
    {
    "id":295,
    "name":"Hà Giang"
    },
    {
    "id":296,
    "name":"Hà Nam"
    },
    {
    "id":299,
    "name":"Hà Tĩnh"
    },
    {
    "id":300,
    "name":"Hải Dương"
    },
    {
    "id":301,
    "name":"Hải Phòng"
    },
    {
    "id":319,
    "name":"Hậu Giang"
    },
    {
    "id":302,
    "name":"Hoà Bình"
    },
    {
    "id":320,
    "name":"Hưng Yên"
    },
    {
    "id":321,
    "name":"Khánh Hòa"
    },
    {
    "id":322,
    "name":"Kiên Giang"
    },
    {
    "id":323,
    "name":"Kon Tum"
    },
    {
    "id":304,
    "name":"Lai Châu"
    },
    {
    "id":306,
    "name":"Lâm Đồng"
    },
    {
    "id":305,
    "name":"Lạng Sơn"
    },
    {
    "id":324,
    "name":"Lào Cai"
    },
    {
    "id":325,
    "name":"Long An"
    },
    {
    "id":326,
    "name":"Nam Định"
    },
    {
    "id":327,
    "name":"Nghệ An"
    },
    {
    "id":307,
    "name":"Ninh Bình"
    },
    {
    "id":328,
    "name":"Ninh Thuận"
    },
    {
    "id":329,
    "name":"Phú Thọ"
    },
    {
    "id":308,
    "name":"Phú Yên"
    },
    {
    "id":309,
    "name":"Quảng Bình"
    },
    {
    "id":310,
    "name":"Quảng Nam"
    },
    {
    "id":311,
    "name":"Quảng Ngãi"
    },
    {
    "id":330,
    "name":"Quảng Ninh"
    },
    {
    "id":312,
    "name":"Quảng Trị"
    },
    {
    "id":313,
    "name":"Sóc Trăng"
    },
    {
    "id":331,
    "name":"Sơn La"
    },
    {
    "id":332,
    "name":"Tây Ninh"
    },
    {
    "id":333,
    "name":"Thái Bình"
    },
    {
    "id":334,
    "name":"Thái Nguyên"
    },
    {
    "id":335,
    "name":"Thanh Hóa"
    },
    {
    "id":303,
    "name":"Thừa Thiên Huế"
    },
    {
    "id":336,
    "name":"Tiền Giang"
    },
    {
    "id":314,
    "name":"Trà Vinh"
    },
    {
    "id":315,
    "name":"Tuyên Quang"
    },
    {
    "id":337,
    "name":"Vĩnh Long"
    },
    {
    "id":338,
    "name":"Vĩnh Phúc"
    },
    {
    "id":339,
    "name":"Yên Bái"
    },
    {
    "id":292,
    "name":"Đắk Lắk"
    },
    {
    "id":340,
    "name":"Đắk Nông"
    },
    {
    "id":341,
    "name":"Điện Biên"
    },
    {
    "id":317,
    "name":"Đồng Nai"
    },
    {
    "id":318,
    "name":"Đồng Tháp"
    }]

def list_product_algorithm(provinces):
    list_product = {}

    users = UserInfo.objects.all()
    for i in provinces:
        for user in users:
            user_province = UserInfo.objects.get(uid=user).province
            if user_province == i:
                products = Product.objects.filter(owner_uid=user)
                for product in products:
                    prod_uid = Product.objects.get(prod_uid=product).prod_uid
                    name = Product.objects.get(prod_uid=product).name
                    description = Product.objects.get(prod_uid=product).description
                    quantity = Product.objects.get(prod_uid=product).quantity
                    current_quantity = Product.objects.get(prod_uid=product).current_quantity
                    price = Product.objects.get(prod_uid=product).price
                    status_percentage = status_calculator(int(current_quantity), int(quantity))
                    status_zone = status_detector(status_percentage)

                    owner_uid = Product.objects.get(prod_uid=product).owner_uid
                    username = UserInfo.objects.get(uid=owner_uid).username
                    province = UserInfo.objects.get(uid=owner_uid).province
                    district = UserInfo.objects.get(uid=owner_uid).district
                    ward = UserInfo.objects.get(uid=owner_uid).ward
                    username = UserInfo.objects.get(uid=owner_uid).username
                    phone_number = UserInfo.objects.get(uid=owner_uid).phone_number


                    list_product[prod_uid] = {}
                    list_product[prod_uid]['owner_uid'] = str(owner_uid)
                    list_product[prod_uid]['prod_uid'] = prod_uid
                    list_product[prod_uid]['prod_name'] = name
                    list_product[prod_uid]['prod_description'] = description
                    list_product[prod_uid]['prod_current_quantity'] = int(current_quantity)
                    list_product[prod_uid]['prod_price'] = int(price)
                    list_product[prod_uid]['prod_status_zone'] = str(status_zone)
                    list_product[prod_uid]['username'] = username
                    list_product[prod_uid]['province'] = province
                    list_product[prod_uid]['district'] = district
                    list_product[prod_uid]['ward'] = ward
                    list_product[prod_uid]['phone_number'] = str(phone_number)

    return list_product

def algorithm_location_near_you(uid, province):
    # get list and sort id.
    province_id=[]
    user_province_id = 0
    for i in data:
        province_id.append(i['id'])
        if i['name'] == province:
            user_province_id = i['id']
    province_id.sort()
    # loop to find the user id.
    index = 0
    for i in province_id:
        if user_province_id == i:
            break
        index += 1
    # from user to start.
    slice_province_rest = province_id[0 : int(index)]
    # from user to end.
    slice_user_province_id=province_id[int(index) : int(len(province_id))]
    # sort to near the user.
    slice_province_rest.sort(reverse=True)
    # join together.
    we_are_one = slice_user_province_id + slice_province_rest
    # action.
    # convert from id to province.
    province_list_complete=[]
    for i in we_are_one:
        for y in data:
            if i == y['id']:
                province_list_complete.append(y['name'])
                break

    # make a list of the user with the given location.
    list_product = list_product_algorithm(province_list_complete)

    return list_product



# return all the bills.
def return_bills_client(bills):
    list_bills = {}

    for bill in bills:
        owner_uid = Bill.objects.get(bill_uid=bill).owner_uid
        client_uid = Bill.objects.get(bill_uid=bill).client_uid
        quantity = Bill.objects.get(bill_uid=bill).quantity
        prod_uid = Bill.objects.get(bill_uid=bill).prod_uid
        status = Bill.objects.get(bill_uid=bill).status

        # get owner name.
        owner_name = UserInfo.objects.get(uid=owner_uid).username
        # get product name.
        product_name = Product.objects.get(prod_uid=prod_uid).name

        list_bills[str(bill)] = {}
        list_bills[str(bill)]['owner_name'] = str(owner_name)
        list_bills[str(bill)]['prod_name'] = str(product_name)
        list_bills[str(bill)]['status'] = str(status)
        list_bills[str(bill)]['quantity'] = int(quantity)

    return list_bills

def return_bills_owner(bills):
    list_bills = {}

    for bill in bills:
        owner_uid = Bill.objects.get(bill_uid=bill).owner_uid
        client_uid = Bill.objects.get(bill_uid=bill).client_uid
        quantity = Bill.objects.get(bill_uid=bill).quantity
        prod_uid = Bill.objects.get(bill_uid=bill).prod_uid
        status = Bill.objects.get(bill_uid=bill).status

        # get client info.
        client_name = UserInfo.objects.get(uid=client_uid).username
        province = UserInfo.objects.get(uid=client_uid).province
        district = UserInfo.objects.get(uid=client_uid).district
        ward = UserInfo.objects.get(uid=client_uid).ward
        phone_number = UserInfo.objects.get(uid=client_uid).phone_number
        # get product name.
        product_name = Product.objects.get(prod_uid=prod_uid).name

        list_bills[str(bill)] = {}
        list_bills[str(bill)]['bill_uid'] = str(bill)
        list_bills[str(bill)]['client_name'] = str(client_name)
        list_bills[str(bill)]['prod_name'] = str(product_name)
        list_bills[str(bill)]['status'] = str(status)
        list_bills[str(bill)]['quantity'] = int(quantity)
        list_bills[str(bill)]['province'] = province
        list_bills[str(bill)]['district'] = district
        list_bills[str(bill)]['ward'] = ward
        list_bills[str(bill)]['phone_number'] = str(phone_number)
    return list_bills




