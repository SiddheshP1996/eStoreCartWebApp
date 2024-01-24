from django.contrib import admin
from eCommWebApp.models import Product

# Register your models here.

# Register ProductAdmin to manipulate the admin panel
class ProductAdmin(admin.ModelAdmin):
    # display in the table format
    list_display = ['id', 'name', 'price', 'product_details', 'category', 'is_active']

    # filter by category
    list_filter = ['category', 'is_active']
    pass

admin.site.register(Product, ProductAdmin)