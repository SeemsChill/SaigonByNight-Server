from django.urls import path
from .views import SBN_User_API_GET_Routes, SBN_User_API_POST_Register_Create_User, SBN_User_API_POST_Register_Update_User,SBN_User_API_DELETE_Specific_User

urlpatterns = [
    path(
        "api/",
        SBN_User_API_GET_Routes.as_view(),
        name="SBN_User_API_GET_Routes."
    ),
    path(
        "api/post/register/create/user/",
        SBN_User_API_POST_Register_Create_User.as_view(),
        name="SBN_User_API_POST_Register_Create_User."
    ),
    path(
        "api/post/register/update/user/",
        SBN_User_API_POST_Register_Update_User.as_view(),
        name="SBN_User_API_POST_Register_Update_User."
    ),
    path(
        "api/delete/user/",
        SBN_User_API_DELETE_Specific_User.as_view(),
        name="SBN_User_API_DELETE_Specific_User."
    )
]
