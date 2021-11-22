from django.contrib import admin
from .models import UserAuth, UserInfo, UserPlatform

# Register your models here.

# User's Platform Tables.
admin.site.register(UserPlatform)

# User's Infor and Auth Tables.
admin.site.register(UserInfo)
admin.site.register(UserAuth)