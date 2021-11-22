# Import Django built-in.
from django.urls import path
# Import SBN_Auth Views.
from .views import SBN_Auth_API_GET_CSRF_Token, SBN_Auth_API_POST_Reset, SBN_Auth_API_GET_Register_Verification, SBN_Auth_API_GET_Reset_Verification, SBN_Auth_API_POST_Submit_Reset

urlpatterns = [
    path(
        "api/get/csrf/",
        SBN_Auth_API_GET_CSRF_Token.as_view(),
        name="SBN_Auth_API_GET_CSRF_Token."
    ),
    path(
        'api/get/verify/register/',
        SBN_Auth_API_GET_Register_Verification.as_view(),
        name='Register email verification handle.'
    ),
    path(
        "api/post/request/reset/",
        SBN_Auth_API_POST_Reset.as_view(),
        name="SBN_Auth_API_POST_Reset."
    ),
    path(
        "api/get/verify/reset/",
        SBN_Auth_API_GET_Reset_Verification.as_view(),
        name="SBN_Auth_API_POST_Reset_Verification."
    ),
    path(
        'api/post/submit/reset/',
        SBN_Auth_API_POST_Submit_Reset.as_view(),
        name='Reset password handle.'
    )
]
