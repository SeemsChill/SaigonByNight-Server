# Import Django built-in.
from django.urls import path
# Import SBN_Auth Views.
from .views import SBN_Auth_API_GET_CSRF_Token

urlpatterns = [
    path(
        "api/get/csrf/",
        SBN_Auth_API_GET_CSRF_Token.as_view(),
        name="SBN_Auth_API_GET_CSRF_Token."
    )
]
