from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import logout as auth_logout
from product.models import Product
from additems.models import addtoCart
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
import json
from django.core.exceptions import ValidationError
import re
from decimal import Decimal, InvalidOperation
from django.db.models import Sum



def homepage(request):
    productdata = Product.objects.all()

    # Handle search filtering
    if request.method == "GET":
        st = request.GET.get('productname')
        if st is not None:
            productdata = productdata.filter(product_title__icontains=st)

    # Set up pagination
    paginator = Paginator(productdata, 12)
    page_num = request.GET.get('page')
    final_data = paginator.get_page(page_num)


    # Get the cart count
    data = {
        'productdata': final_data,
        
        
    }

    return render(request, "homepage.html", data)




def sign(request):
    if request.method == 'POST':
        firstname = request.POST['first-name']
        lastname = request.POST['last-name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['repeat-password']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "sign_in.html", {
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'username': username,
            })

        try:
            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=username,
                password=password1
            )
            user.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "An error occurred: " + str(e))

            return render(request, "sign_in.html")

    return render(request, "sign_in.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password']

        # Authenticate user
        user = auth.authenticate(username=username, password=password1)

        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")



def logout(request):
    if request.method == 'POST':
        auth_logout(request)  # User ko logout karein
        return redirect('login')  # Login page par redirect karein
    return render(request, "logout.html")  # Logout confirmation page dikhao

def head(request):
    return render(request, "head.html")

def foot(request):
    return render(request, "foot.html")

def cart(request):
    # Your logic for the cart
    return render(request, 'cart.html')


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        title = product.product_title
        image = product.product_img.url
        price_html = product.product_price
        quantity = int(request.POST.get('quantity', 1))  # Ensure quantity is an integer

        # Clean the price to convert it to a decimal
        price_str = re.sub(r'<[^>]+>', '', price_html)
        price_str = price_str.replace("Rs.", "").strip()
        try:
            price = Decimal(price_str)
        except InvalidOperation:
            raise ValidationError("Invalid price format.")

        # Check if item already exists in the cart
        existing_item = addtoCart.objects.filter(product_id=product.id).first()
        if existing_item:
            existing_item.product_quantity += quantity  # Update existing quantity
            existing_item.save()
        else:
            # Create a new cart item
            cart_item = addtoCart(
                product_id=product,
                product_title=title,
                product_img=image,
                product_price=price,
                product_quantity=quantity
            )
            cart_item.save()

        messages.success(request, f"{title} has been added to your cart.")  # Success message
        return redirect('homepage')

    return redirect('homepage')

def view_cart(request,):

    data = addtoCart.objects.all()
    return render(request, 'cart.html', {'cart_items': data})

from django.db.models import Sum

def cart_count(request):
    total_count = addtoCart.objects.aggregate(total=Sum('quantity'))['total'] or 0
    return total_count
