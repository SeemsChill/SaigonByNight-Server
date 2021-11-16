from django.urls import path
from .views import SBN_User_API_POST_Register_Create_User, SBN_User_API_POST_Login, SBN_User_API_POST_Register_Update_User, SBN_User_API_POST_Forgot, SBN_User_API_DELETE_Specific_User, SBN_User_API_POST_Verification

urlpatterns = [
    path(
        "api/post/register/user/",
        SBN_User_API_POST_Register_Create_User.as_view(),
        name="SBN_User_API_POST_Register_Create_User."
    ),
    path(
        "api/post/login/",
        SBN_User_API_POST_Login.as_view(),
        name="SBN_User_API_POST_Login."
    ),
    path(
        "api/post/register/update/user/",
        SBN_User_API_POST_Register_Update_User.as_view(),
        name="SBN_User_API_POST_Register_Update_User."
    ),
    path(
        "api/post/forgot/",
        SBN_User_API_POST_Forgot.as_view(),
        name="SBN_User_API_POST_Forgot."
    ),
    path(
        "api/delete/user/",
        SBN_User_API_DELETE_Specific_User.as_view(),
        name="SBN_User_API_DELETE_Specific_User."
    ),
    path(
        "api/post/verification/",
        SBN_User_API_POST_Verification.as_view(),
        name="SBN_User_API_POST_Verification."
    ),
]


