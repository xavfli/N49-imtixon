from django.db import models

from app_user.models import UserModel, Customer
# from app_product.models import Cart, Product
from django.shortcuts import get_object_or_404, redirect

# from app_user.views import User

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Category name')
    image = models.ImageField(upload_to='media/category')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.title}'



class Product(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Product name')
    image = models.ImageField(upload_to='media/product')
    description = models.TextField()
    old_price = models.CharField(max_length=50, blank=True)
    price = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    sale = models.BooleanField()

    def __str__(self):
        return f'{self.category},{self.title}'




class CartItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product_id'], name='unique_user_product')
        ]

    @property
    def total_price(self):
        return self.quantity * self.product.price


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user}"
