from django.urls import path
from .views import CreateProduct, GetListProduct, UpdateProduct, DeleteProduct, ListAllTheProduct, BuyTheProduct, GetAllBillsForClient, GetAllBillsForOwner, BillAction

urlpatterns = [
    path('api/get/list/product/', GetListProduct.as_view(), name='Get all list involving with the current user.'),
    path('api/post/create/product/', CreateProduct.as_view(), name='Create a produdct.'),
    path('api/post/update/product/', UpdateProduct.as_view(), name='Update a product.'),
    path('api/post/delete/product/', DeleteProduct.as_view(), name='Delete a product'),
    path('api/get/all/product/', ListAllTheProduct.as_view(), name='List all the product.'),
    path('api/post/buy/product/', BuyTheProduct.as_view(), name='buy the product.'),
    path('api/get/all/client/bills/', GetAllBillsForClient.as_view(), name='get all bills'),
    path('api/get/all/owner/bills/', GetAllBillsForOwner.as_view(), name='get all bills for owner.'),
    path('api/get/action/bill/', BillAction.as_view(), name='action to the bill.')
]

