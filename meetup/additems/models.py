from django.db import models
from product.models import Product  # Assuming the Product model exists

# Create your models here.
class addtoCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product model
    product_title = models.CharField(max_length=255)
    product_img = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)

   
