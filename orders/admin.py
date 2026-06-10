from django.contrib import admin
from .models import OrderItem, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "first_name", "last_name", "status", "created_at"]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "book", "price", "quantity"]

