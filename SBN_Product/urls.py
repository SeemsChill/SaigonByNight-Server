from django.urls import path
from .views import GetListProduct

urlpatterns = [
    path('api/get/list/product/', GetListProduct.as_view(), name='Get all list involving with the current user.')
]
