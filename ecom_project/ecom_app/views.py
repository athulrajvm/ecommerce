from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login,logout
from .models import *
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



# Create your views here.


def home(request):

    return render(request,'home.html')

def loginpage(request):

    return render(request,'loginpage.html')

def logfun(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:  # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('adminhome')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('customerhome')  # Redirect to techhome after login
            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('loginpage')

            
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('loginpage')
    return render(request, 'loginpage.html')

def signuppage(request):
    
    return render(request,'signuppage.html')

def usercreate(request):
    if request.method=='POST': 
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        age=request.POST['age']
        address=request.POST['add']
        phoneno=request.POST['ph']
        username=request.POST['uname']
        password=request.POST['fpass']
        cpassword=request.POST['npass']
        email=request.POST['email']
        img = request.FILES.get('img')
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists')
                return redirect('signuppage')
            if not email.endswith('@gmail.com'):
                messages.error(request, "Email must be a @gmail.com address.")
                return redirect('signuppage')
            if len(phoneno) != 10 or not phoneno.isdigit():
                messages.error(request, "Phone number must be exactly 10 digits.")
                return redirect('signuppage')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('signuppage')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
                user.save()
                u = User.objects.get(id=user.id)
                t = Customer(address=address,age=age,phone=phoneno,user=u,image=img)
                t.save()
                messages.info(request,'user successfully registered')
                return redirect("loginpage")
                
        else:
            messages.info(request,'Password doesnot match')
            return redirect('signuppage')
        
    else:
        return render(request,'signuppage.html')
    
@login_required(login_url='loginpage')   
def adminhome(request):
    
    return render(request,'adminhome.html')

@login_required(login_url='loginpage')
def customerhome(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'customerhome.html',{"categories":categories,"products":products})

@login_required(login_url='loginpage')
def add_category(request):
    return render(request,'add_category.html')

@login_required(login_url='loginpage')
def categoryfun(request):
    if request.method == 'POST':
        category = request.POST['cate']
        c = Category(categoryname=category)
        c.save()
        messages.info(request,'added successfully')
        return redirect("add_category")
    
@login_required(login_url='loginpage')
def category_page(request, category_id):
    categories = Category.objects.all()
    products = Product.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_page.html', {
        'category': category,
        'products': products,
        "categories":categories,
        "products":products
    })

@login_required
def add_product(request):
    c = Category.objects.all()
    return render(request,'add_product.html',{"category":c})

def productfun(request):
    if request.method == 'POST':
        prdtname = request.POST['pname']
        despn = request.POST['des']
        pri = request.POST['price']
        category = request.POST['cate']
        c = Category.objects.get(id=category)
        imgg = request.FILES.get('img')
        p = Product(productname=prdtname,description=despn,price=pri,image=imgg,category=c)
        p.save()
        messages.info(request,'added successfully')
        return redirect("add_product")
    
@login_required   
def view_product(request):
    pro = Product.objects.all()
    return render(request,'view_product.html',{"prt":pro})

@login_required
def edit_product(request,pk):
    pd = Product.objects.get(id=pk)
    c = Category.objects.all()
    return render(request,'edit_product.html',{"prd":pd,"cate":c})

@login_required
def editproduct(request,p):
    if request.method == "POST":
        pd = Product.objects.get(id=p)
        pd.productname=request.POST.get("pname")
        pd.description=request.POST.get("des")
        pd.price=request.POST.get("price")
        ct = request.POST.get("cate")
        c = Category.objects.get(id=ct)
        pd.category = c
        newimage = request.FILES.get("img")
        if newimage:
            if pd.images:
                os.remove(pd.images.path)
                pd.images = newimage
        pd.save()
        return redirect("view_product")
    return render(request,'edit_product.html')


def delete_product(request,p):
    pd = Product.objects.get(id=p)
    pd.delete()
    return redirect("view_product")

@login_required
def view_user(request):
    cus = Customer.objects.all()
    return render(request,'view_user.html',{"ct":cus})

def delete_user(request,p):
    ct = Customer.objects.get(id=p)
    user = ct.user
    ct.delete()
    user.delete()
    return redirect("view_user")

def logoutfun(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request,'logout successfully')
    return redirect('home')


def edit_user(request,pk):
    u = Customer.objects.get(id=pk)
    return render(request,'edit_user.html',{"ur":u})

@login_required
def edituser(request,p):
    if request.method == "POST":
        u = Customer.objects.get(id=p)
        u.age=request.POST.get("age")
        u.address=request.POST.get("address")
        u.phone=request.POST.get("phone")
        newimage = request.FILES.get("img")
        if newimage:
            if u.images:
                os.remove(u.images.path)
                u.images = newimage
        u.save()
        return redirect("customerhome")
    return render(request,'edituser.html')

@login_required
def edituser(request):
    c = Customer.objects.get(user=request.user)
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,'edituser.html',{"cus":c,"categories":categories,"products":products})

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
import os
from .models import Customer
from django.contrib.auth.models import User

def user_update(request, tr):
    if request.method == 'POST':
        c = Customer.objects.get(user=tr)
        user = User.objects.get(id=tr)

        # Collect data from the request
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        address = request.POST['add']
        age = request.POST['age']
        phone = request.POST['ph']
        new_image = request.FILES.get('img')

        # Validation
        if User.objects.filter(Q(username=username) & ~Q(id=tr)).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('edituser')

        if User.objects.filter(Q(email=email) & ~Q(id=tr)).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('edituser')

        if not email.endswith('@gmail.com'):
            messages.error(request, 'Email must be a @gmail.com address.')
            return redirect('edituser')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, 'Phone number must be exactly 10 digits.')
            return redirect('edituser')

        # Save the updated data
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        c.address = address
        c.age = age
        c.phone = phone

        if new_image:
            # Delete old image if exists
            if c.image:
                if os.path.exists(c.image.path):
                    os.remove(c.image.path)
            c.image = new_image

        c.save()
        messages.info(request, 'Updated successfully.')
        return redirect('edituser')
    
def aboutus(request):
    return render(request,'aboutus.html')

def menshoes(request):
    return render(request,'menshoes.html')

def womenshoes(request):
    return render(request,'womenshoes.html')

def kidshoes(request):
    return render(request,'kidshoes.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.create(user=request.user, product=product)
    return redirect('customerhome')



@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items = Cart.objects.all()
    for item in cart_items:
        item.total_price = item.quantity * item.product.price

    return render(request, 'cart.html', {'cart_items': cart_items})
    

def update_quantity(request, item_id):
    if request.method == "POST":
        action = request.POST.get("action")
        cart_item = get_object_or_404(Cart, id=item_id)

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        return JsonResponse({
            "quantity": cart_item.quantity,
            "total_price": cart_item.total_price(),
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def cart_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    totals_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': totals_price,
        "categories":categories,
        "products":products
    })












