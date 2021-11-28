# Import system.
import os
from uuid import uuid4
# Import django modules.
from django.utils.deconstruct import deconstructible
from django.db import models
# Import User models.
from SBN_User.models import UserInfo

# Create your models here.

@deconstructible
class ImageProductPath(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}/products/{}.{}'.format(
                instance.prod_uid,
                instance.pk,
                ext
            )
        else:
            filename = '{}/products/{}.{}'.format(
                instance.prod_uid,
                uuid4().hex,
                ext
            )
        return os.path.join(
            self.path,
            filename
        )

class Category(models.Model):
    category = models.CharField(
        # Attributes.
        max_length=20,
        unique=True,
        # Details.
        verbose_name="product_category.",
        help_text="Following format: char(1 -> 20)."
    )

    class Meta:
        verbose_name = "product_category."
        verbose_name_plural = "product_categories."

    def __str__(self):
        return str(self.category)


class Product(models.Model):
    owner_uid = models.ForeignKey(
        # Connection.
        UserInfo,
        on_delete=models.CASCADE,
        # Details.
        verbose_name="owner_uid.",
        help_text="Following format: char(1 -> 38).",
    )
    prod_uid = models.CharField(
        # Attributes.
        max_length=32,
        # Details.
        verbose_name="product_uid.",
        help_text="Following format: char(1 -> 32)."
    )
    # Details:
    name = models.CharField(
        # Attributes.
        max_length=40,
        # Details.
        verbose_name="product_name.",
        help_text="Following format: char(1 -> 40)."
    )
    category = models.ForeignKey(
        # Connection.
        Category,
        on_delete=models.CASCADE,
        # Details.
        verbose_name="product_category.",
        help_text="Following format: char(1 -> 38)."
    )
    description = models.TextField(
        # Details.
        verbose_name="product_description.",
        help_text="Following format: char(1 -> 40)."
    )
    price = models.DecimalField(
        # Attributes.
        max_digits=30,
        decimal_places=15,
        # Details.
        verbose_name="product_price.",
        help_text="Following format: dec(1 -> 30:15)."
    )
    discount = models.DecimalField(
        # Attributes.
        max_digits=30,
        decimal_places=15,
        # Details.
        verbose_name="product_discount.",
        help_text="Following format: dec(1 -> 30:15)."
    )
    graph = models.CharField(
        # Attributes.
        max_length=1000,
        # Details.
        verbose_name="For using later.",
        help_text="Following format: char(1 -> 1000)."
    )
    quantity = models.DecimalField(
        # Attributes.
        max_digits=30,
        decimal_places=15,
        # Details.
        verbose_name="product_quantity.",
        help_text="Following format: dec(1 -> 30:15)."
    )
    current_quantity = models.DecimalField(
        # attributes.
        max_digits = 30,
        decimal_places=15,
        # details.
        verbose_name='current_quantity.',
        help_text='following format: dec(1 -> 30:15).'
    )
    status = models.BooleanField(
        # Attributes.
        default=True,
        # Details.
        verbose_name="product_status?",
        help_text="products still have?"
    )
    image = models.ImageField(
        # Attributes.
        upload_to=ImageProductPath('images/'),
        # Details.
        verbose_name='product_image.',
        help_text='Your product image link.',
    )

    class Meta:
        verbose_name = "product."
        verbose_name_plural = "products."

    def __str__(self):
        return str(self.prod_uid)


class Bill(models.Model):
    owner_uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        verbose_name='owner_uid',
        help_text='Following format: char(1->38).',
        related_name='owner_uid'
    )
    prod_uid = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='product_uid',
        help_text='Following format: char(1 -> 32).'
    )
    client_uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        verbose_name='owner_uid',
        help_text='Following format: char(1->38).',
        related_name='client_uid'
    )

    status = models.BooleanField(
        default=False,
        verbose_name='product_status',
        help_text='thanh toan?'
    )

    class Meta:
        verbose_name = "bill."
        verbose_name_plural = 'bills.'

    def __str__(self):
        return str(self.prod_uid)
