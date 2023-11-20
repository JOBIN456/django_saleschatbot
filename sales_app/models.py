from django.db import models
from django.conf import settings
# Create your models here.
#THIS IS THE MODEL FOR PRODUCTS
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
#MODEL FOR CART
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
#MODEL FOR CARTITEM
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'