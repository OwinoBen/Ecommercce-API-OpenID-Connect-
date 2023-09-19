from django.contrib import admin

from orders.models import PurchasedProducts
from .models import Product


@admin.register(Product)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("product_title", "product_qty", "selling_price", "discount_price", "is_verified", "created_date")
    search_fields = ("product_title", "selling_price", "discount_price", "is_verified")
    ordering = ("-created_date",)
    readonly_fields = ['created_date', 'product_sku', 'updated_date']


@admin.register(PurchasedProducts)
class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ("order", 'product', 'refunded', 'created_at')
    search_fields = ("order", "refunded")
    ordering = ("-created_at",)



