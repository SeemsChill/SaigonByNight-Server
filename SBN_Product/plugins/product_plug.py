# models.
from ..models import Product
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
