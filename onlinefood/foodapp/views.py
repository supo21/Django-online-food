from django.contrib import messages
import random
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    queryset = list(Item.objects.all())
    featured_items = random.sample(queryset, 4)
    context = {"featured_items": featured_items}

    queryset = Item.objects.all()

    if request.GET.get("search"):
        queryset = queryset.filter(item_name__icontains = request.GET.get("search"))

        context = {"items": queryset}

        return render(request, "items.html", context)

    return render(request, "home.html", context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username ).exists:
            messages.error(request, "Invalid Username.")
            return redirect('/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect("/register/") 

        user = User.objects.create(
            first_name= first_name, 
            last_name= last_name,
            username= username, 
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect("/register/")

    return render(request, "register.html")
    
@login_required(login_url= "/login/")
def add_cart(request, item_uid):
    user = request.user
    item_obj = Item.objects.get(uid = item_uid)
    cart , created = Cart.objects.get_or_create(user= user, is_paid = False)

    cart_items , created = CartItems.objects.get_or_create(
        cart = cart,
        item = item_obj,
    )

    if not created:
        cart_items.quantity += 1
        cart_items.save()
    else:
        cart_items.save()                       
                                          
    return redirect('/')

@login_required(login_url= "/login/")
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False,user= request.user)
        cartItems = CartItems.objects.filter(cart = cart)
        if not cartItems.exists():
            context = {'carts' : cart,'cart_items':None, 'total_amount':None}
        else:
            total_amount = cart.get_cart_total()
            if total_amount is None:
                context = {'carts' : cart,'cart_items':cartItems, 'total_amount': None}
            else:
                context = {'carts' : cart,'cart_items':cartItems, 'total_amount': total_amount+10}
    except Cart.DoesNotExist:
        context = {'carts' : None,'cart_items':None, 'total_amount':None}
   

    return render(request, 'cart.html', context)

@login_required(login_url= "/login/")
def remove_cart_items(request, cart_item_uid):
    try:
        CartItems.objects.get(uid = cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)

@login_required(login_url= "/login/")
def orders(request):
    orders = Cart.objects.filter(is_paid = True, user= request.user)
    context = {'orders':orders}
    if request.GET.get("search"):
        queryset = queryset.filter(item_name__icontains = request.GET.get("search"))

        context = {"items": queryset}

        return render(request, "items.html", context)
    return render(request, 'orders.html', context)

@login_required(login_url= "/login/")
def add_item(request):
    if request.method == "POST":
        data = request.POST

        item_name = data.get("item_name")
        description = data.get("description")
        category= data.get("category")
        price = data.get("price")
        image = request.FILES.get("image")
        
        Item.objects.create(
            item_name = item_name,
            description = description,
            category = category,
            price = price,
            image = image,
        )

        return redirect('/all-items/')
    
    return render(request, 'add_item.html')
    

def all_items(request):
    all_items = Item.objects.all()
    context = {"items": all_items}

    if request.GET.get("search"):
        queryset = queryset.filter(item_name__icontains = request.GET.get("search"))

        context = {"items": queryset}

        return render(request, "items.html", context)

    return render(request, "items.html", context)

@login_required(login_url= "/login/")
def delete_item(request, item_uid):
    queryset = Item.objects.get(uid = item_uid)
    queryset.delete()
    return redirect("/all-items/")

@login_required(login_url= "/login/")
def update_item(request, item_uid):
    queryset = Item.objects.get(uid = item_uid)

    if request.method == "POST":
        data = request.POST
        item_name = data.get("item_name")
        description = data.get("description")
        category = data.get("category")
        price = data.get("price")
        image = request.FILES.get("image")
        

        queryset.item_name = item_name
        queryset.description = description
        queryset.category = category
        queryset.price = price
        if image:
            queryset.image = image

        queryset.save()
        return redirect("/all-items/")

    context = {"item" : queryset}
    return render(request, "update_items.html", context)

def success(request):
    cart = Cart.objects.get(user= request.user, is_paid = False)
    cart.is_paid = True
    cart.save()
    return render(request, "success.html")

def all_orders(request):
    return render(request, 'all_orders.html')