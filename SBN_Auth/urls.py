# Import Django built-in.
from django.urls import path
# Import SBN_Auth Views.
from .views import SBN_Auth_API_GET_CSRF_Token, SBN_Auth_API_POST_Reset, SBN_Auth_API_POST_Reset_Verification

urlpatterns = [
    path(
        "api/get/csrf/",
        SBN_Auth_API_GET_CSRF_Token.as_view(),
        name="SBN_Auth_API_GET_CSRF_Token."
    ),
    path(
        "api/post/reset/",
        SBN_Auth_API_POST_Reset.as_view(),
        name="SBN_Auth_API_POST_Reset."
    ),
    path(
        "api/post/reset/verification/",
        SBN_Auth_API_POST_Reset_Verification.as_view(),
        name="SBN_Auth_API_POST_Reset_Verification."
    )
]
