from django.contrib import admin
from .models import Category, Product

# Register your models here.

# Product's Platform Tables.
admin.site.register(Category)
admin.site.register(Product)
