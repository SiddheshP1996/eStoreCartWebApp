from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django import forms
"""
class Demo(forms.Form):
    name = forms.CharField(max_length = 20)
    email = forms.CharField(max_length = 30)
    pass
"""

class Product(models.Model):
    # Dictionary to showcase the category names instead of numbers
    CAT = ((1, 'Mobile'), (2, 'Shoes'), (3, 'Cloth'))

    name = models.CharField(max_length = 20, verbose_name = 'Product Name')
    price = models.FloatField(max_length = 30, verbose_name = 'Product Price')
    product_details = models.CharField(max_length = 50)
    category = models.IntegerField(choices = CAT)
    is_active = models.BooleanField(default  = True, verbose_name = 'Available')
    pimage = models.ImageField(upload_to = 'image')

    # Will display as a table in the admin panel using below function
    def __str__(self):
        return self.name


class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'uid')
    pid = models.ForeignKey(Product, on_delete = models.CASCADE, db_column = 'pid')
    qty = models.IntegerField(default = 1)

class Order(models.Model):
    order_id = models.CharField(max_length = 50)
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column = 'uid')
    pid = models.ForeignKey(Product, on_delete = models.CASCADE, db_column = 'pid')
    qty = models.IntegerField(default = 1)

