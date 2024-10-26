from django.contrib import admin

from product.models import Product  # Make sure to import the correct model name

class productAdmin(admin.ModelAdmin):
    list_display = ('product_title','product_img',  'product_price','product_quantity')  # Ensure these fields exist in your model

# Register the model with the admin site
admin.site.register(Product, productAdmin)
