from django.contrib import admin
from additems.models import addtoCart

class addtoCartAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'product_price', 'product_quantity', 'quantity') 

