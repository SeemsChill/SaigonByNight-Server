from django.db import models
from django.utils.deconstruct import deconstructible
from phonenumber_field.modelfields import PhoneNumberField
import os
from uuid import uuid4


@deconstructible
class ImageAvatarPath(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}/avatars/{}.{}'.format(
                instance.uid,
                instance.pk,
                ext
            )
        else:
            filename = '{}/avatars/{}.{}'.format(
                instance.uid,
                uuid4().hex,
                ext
            )
        return os.path.join(
            self.path,
            filename
        )


@deconstructible
class ImageBackgroundPath(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        if instance.pk:
            filename = '{}/backgrounds/{}.{}'.format(
                instance.uid,
                instance.pk,
                ext
            )
        else:
            filename = '{}/backgrounds/{}.{}'.format(
                instance.uid,
                uuid4().hex,
                ext
            )
        return os.path.join(
            self.path,
            filename
        )


class UserPlatform(models.Model):  # User's Platform Table.
    platform = models.CharField(
        # Attributes.
        max_length=20,
        # Details.
        verbose_name="user_category.",
        help_text="Following format: char(1 -> 20).",
    )

    class Meta:
        verbose_name = "user_platform."
        verbose_name_plural = "user_platforms."

    def __str__(self):
        return self.platform


class UserInfo(models.Model):  # User's Information Table.
    uid = models.CharField(
        # Attributes.
        max_length=28,
        unique=True,
        # Details.
        verbose_name="user_uid.",
        help_text="Following format: char(1 -> 28).",
        primary_key=True
    )
    username = models.CharField(
        # Attributes.
        max_length=20,
        # Details.
        verbose_name="user_username.",
        help_text="Following format: char(1 -> 20).",
    )
    email = models.EmailField(
        # Attributes.
        max_length=40,
        unique=True,
        # Details.
        verbose_name="user_email.",
        help_text="Following format: char(1 -> 40).",
    )
    platform = models.ForeignKey(
        # Connection.
        UserPlatform,
        on_delete=models.CASCADE,
        # Details.
        verbose_name="user_platform.",
        help_text="Each User Tables (UserInfo and UserAuth) have only 1 platform.",
    )
    full_name = models.CharField(
        # Attributes.
        max_length=40,
        # Details.
        verbose_name="full_name.",
        help_text="Following format: char(1 -> 40).",
    )
    province = models.CharField(
        # Attributes.
        max_length=40,
        # Details.
        verbose_name="first_destination.",
        help_text="Following format: char(1 -> 40).",

    )
    district = models.CharField(
        # Attributes.
        max_length=40,
        # Details.
        verbose_name="second_destination.",
        help_text="Following format: char(1 -> 40).",
    )
    ward = models.CharField(
        # Attributes.
        max_length=40,
        # Details.
        verbose_name="third_destination.",
        help_text="Following format: char(1 -> 40).",
    )
    # Detail address:
    detail_adr = models.TextField(
        # Attributes.
        max_length=200,
        # Details.
        verbose_name="detail_address.",
        help_text="Following format: char(1 -> 40).",
    )
    phone_number = PhoneNumberField()
    avatar = models.ImageField(
        # Attributes.
        upload_to=ImageAvatarPath("images/"),
        default="images/default/avatar.png",
        # Details.
        verbose_name="avatar_image.",
        help_text="Your avatar image link.",
    )
    avatar_alt = models.CharField(
        # Attributes.
        max_length=200,
        # Details.
        verbose_name="avatar_alt_text.",
        help_text="Following format: char(1 -> 200)."
    )
    background = models.ImageField(
        # Attributes.
        upload_to=ImageBackgroundPath("images/"),
        default="images/default/background.png",
        # Details.
        verbose_name="background_image.",
        help_text="Your background image link.",
    )
    background_alt = models.CharField(
        # Attributes.
        max_length=200,
        # Details.
        verbose_name="background_alt_text.",
        help_text="Following format: char(1 -> 200)."
    )

    class Meta:
        verbose_name = "user_uid."
        verbose_name_plural = "user_uids."

    def __str__(self):
        return self.uid


class UserAuth(models.Model):  # User's Auth Table.
    uid = models.ForeignKey(
        # Connection.
        UserInfo,
        on_delete=models.CASCADE,
        # Details.
        verbose_name="user_uid.",
        help_text="Following format: char(1 -> 28).",
    )
    username = models.CharField(
        # Attributes.
        max_length=20,
        # Details.
        verbose_name="user_username.",
        help_text="Following format: char(1 -> 20)."
    )
    email = models.EmailField(
        # Attributes.
        max_length=40,
        unique=True,
        # Details.
        verbose_name="user_email.",
        help_text="Following format: char(1 -> 40)."
    )
    password = models.CharField(
        # Attributes.
        max_length=64,
        # Details.
        verbose_name="user_password.",
        help_text="Hashed password using SHA-256. char(64)."
    )
    is_verified = models.BooleanField(
        # Attributes.
        default=False,
        # Details.
        verbose_name="user_verified?",
        help_text="Account has been verified?"
    )
    is_reset = models.BooleanField(
        # Attributes.
        default=False,
        # Details.
        verbose_name="has_reset_password?",
        help_text="Password has been reset?"
    )

    class Meta:
        verbose_name = "user_auth."
        verbose_name_plural = "user_auths."

    def __str__(self):
        return str(self.uid)
