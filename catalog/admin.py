from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "status", "owner")
    list_filter = ("status",)
    search_fields = ("name", "description")
