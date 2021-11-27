from django.urls import path
from .views import CreateProduct, GetListProduct

urlpatterns = [
    path('api/get/list/product/', GetListProduct.as_view(), name='Get all list involving with the current user.'),
    path('api/post/create/product/', CreateProduct.as_view(), name='Create a produdct.'),
]
