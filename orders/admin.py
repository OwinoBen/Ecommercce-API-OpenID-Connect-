from django.contrib import admin

from .models import Orders, OrderItems


@admin.register(Orders)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("order_id", "order_status", "active", "payment_mode", "created_at")
    search_fields = ("order_id", "order_status", "payment_mode")
    ordering = ("-created_at",)
    readonly_fields = ['created_at', 'order_id']


@admin.register(OrderItems)
class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ("order", 'ordered', 'quantity', 'created_at')
    search_fields = ("order", "ordered")
    ordering = ("-created_at",)



