from django.contrib import admin

from .models import Product, Customer, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'uuid', 'date_updated', 'is_active', )
    list_filter = ('is_active', )
    date_hierarchy = 'date_updated'
    search_fields = ['uuid', 'name', ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', )
    search_fields = ['name', 'email', 'phone', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'price', 'confirmation', )
