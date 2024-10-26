from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField

class Product(models.Model):

    product_title = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='app_images/') 
    product_price = HTMLField()
    product_quantity = models.IntegerField(default=1)  # IntegerField for quantity

    product_slug=AutoSlugField(populate_from='product_title',unique=True,null=True,blank=True,default=None)
