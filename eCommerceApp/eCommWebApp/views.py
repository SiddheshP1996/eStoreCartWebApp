from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from eCommWebApp.models import Product, Cart, Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    context = {}
    context['name'] = "John"
    context['age'] = 20
    context['x'] = 100
    context['y'] = 20
    context['l'] = [10, 20, 30, 40, "Siddhesh Panajkar", "Dhananjat Wagh"]
    context['products'] = [
        {'id': 1, 'name': 'samsung', 'cat': 'mobile', 'price': 20000},
        {'id': 2, 'name': 'jeans', 'cat': 'cloth', 'price': 500},
        {'id': 3, 'name': 'adidas shoes', 'cat': 'shoes', 'price': 3000},
        {'id': 4, 'name': 'vivo', 'cat': 'mobile', 'price': 15000},
    ]
    if context['x'] > context['y']:
        # return HttpResponse("X is Greater.")
        context['res'] = "X is Greater."
    else:
        # return HttpResponse("Y is Greater.")
        context['res'] = "Y is Greater."
    # return HttpResponse("<i>This is Home Page.</i>")
    return render(request, 'home.html', context)

def home2(request):
    # userId = request.user.id
    # print("Id of logged-in user : ", userId)
    # print("Result: ", request.user.is_authenticated)
    context = {}
    p = Product.objects.filter(is_active = True)
    # print(p)
    # print(p[0])
    # print(p[0].price)
    # print(p[0].category)
    context['products'] = p
    return render(request, 'index.html', context)

# Below function will return all active and inactive products
def home3(request):
    context = {}
    p = Product.objects.all()
    context['products'] = p
    return render(request, 'index.html', context)

"""
def all(request):
    context = {}
    p = Product.objects.all()
    context['products'] = p
    return render(request, 'index.html', context)
"""

def category_filter(request, cv):
    # cv = category value
    q1 = Q(is_active = True)
    q2 = Q(category = cv)
    p = Product.objects.filter(q1 & q2)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)

def range(request):
    min = request.GET['min']
    max = request.GET['max']
    # print(min)
    # print(max)
    q1 = Q(price__gte = min)
    q2 = Q(price__lte = max)
    q3 = Q(is_active = True)
    p = Product.objects.filter(q1 & q2 & q3)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)

def sort(request, sv):
    # sv = sort value
    # print(type(sv))
    if sv == '0':
        col = 'price'
    else:
        col = '-price'
    p = Product.objects.filter(is_active = True).order_by(col)
    context = {}
    context['products'] = p
    return render(request, 'index.html', context)

def registration(request):
    context = {}
    if request.method == 'POST':
        uname = request.POST['uname']
        upassword = request.POST['upassword']
        uconfirmpassword = request.POST['uconfirmpassword']
        if uname == "" or upassword == "" or uconfirmpassword == "":
            context['errormsg'] = "Fields Cannot be Empty"
            return render(request, 'registration.html', context)
        elif upassword != uconfirmpassword:
            context['errormsg'] = "Password and Confirm Password did not match."
            return render(request, 'registration.html', context)
        else:
            try:
                # u = User.objects.create(password = upassword, username = uname, email = uname)
                u = User.objects.create(username = uname, email = uname)
                u.set_password(upassword)
                u.save()
                context['success'] = "User Created Successfully !"
                return render(request, 'registration.html', context)
            except Exception:
                context['errormsg'] = "User with same username already exists."
                return render(request, 'registration.html', context)
            # return HttpResponse("User Created Successfully !!")
        pass
    else:
        return render (request, 'registration.html', context)
    # return render(request, 'registration.html')


def dummyRegistration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
    return render (request, 'dummyRegistration.html', {'form':form})

def user_login(request):
    context = {}
    if request.method == "POST":
        uname = request.POST['uname']
        upassword = request.POST['upassword']
        if uname == "" or upassword == "":
            context['errormsg'] = "Fields Cannot be Empty"
        else:
            u = authenticate(username = uname, password = upassword)
            """
            print(u)
            print(u.email)
            print(u.is_superuser)
            return HttpResponse("In the Else part")
            """
            if u is not None:
                # start session and store id od logged-in user
                login(request, u)
                return redirect('/home2')
            else:
                context['errormsg'] = "Invalid Username or Password"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

def password_reset(request):
    context = {}
    if request.method == 'POST':
        uname = request.POST['uname']
        newpassword = request.POST['newpassword']
        confirmnewpassword = request.POST['confirmnewpassword']
        if uname == "" or newpassword == "" or confirmnewpassword == "":
            context['errormsg'] = "Fields cannot be Empty"
            return render(request, 'password_reset.html', context)
        elif newpassword != confirmnewpassword:
            context['errormsg'] = "Enter Same Password for both inputs"
            return render(request, 'password_reset.html', context)
        else:
            try:
                u = User.objects.get(username = uname)
                u.set_password(confirmnewpassword)
                u.save()
                context['success'] = "Password Updated / Changed Successfully !!"
                return render(request, 'password_reset.html', context)
            except Exception:
                context['errormsg'] = "Enter Same Password for both inputs"
                return render(request, 'password_reset.html', context)
    else:
        return render(request, 'password_reset.html', context)

def user_logout(request):
    logout(request)
    # context = {}
    # context['title1'] = "logout"
    # demo()
    # return render(request, 'header.html', context)
    return redirect('/home2')

"""
def demo(request):
    return redirect('/home2')
"""

def product_detail(request, pid):
    context = {}
    context['products'] = Product.objects.filter(id = pid)
    return render(request, 'product_detail.html', context)

def addtocart(request, pid):
    if request.user.is_authenticated:
        # print("User is logged in")
        # return HttpResponse("User logged in")
        u = User.objects.filter(id = request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].username)
        # print(u[0].is_superuser)
        p = Product.objects.filter(id = pid)
        # print(p)
        # return HttpResponse("Product is added in cart")
        # check product exists or not
        q1 = Q(uid = u[0])
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)
        print(c)
        n = len(c)
        print(n)
        context = {}
        context['products'] = p
        # Print message if product is equal to one or add the product in tha table if product is not added in the cart
        if n == 1:
            context['msg'] = "Product Already Exists in Cart !!"
        else:
            c = Cart.objects.create(uid = u[0], pid = p[0])
            c.save()
            context['success'] = "Product Added Successfully to Cart !!"
        return render(request, 'product_detail.html', context)
    else:
        return redirect('/login')

def place_order(request):
    userid = request.user.id
    c = Cart.objects.filter(uid = userid)
    # print(c)
    oid = random.randrange(1000, 9999)
    print("Order Id :", oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o = Order.objects.create(order_id = oid, pid = x.pid, uid  = x.uid, qty = x.qty)
        o.save()
        x.delete()
    orders = Order.objects.filter(uid = request.user.id)
    summation = 0
    numberProducts = len(orders)
    for x in orders:
        summation = summation + x.pid.price * x.qty
    context = {}
    context['products'] = orders
    context['total'] = summation
    context['np'] = numberProducts
    return render(request, 'place_order.html', context)

def cart(request):
    userid = request.user.id
    c = Cart.objects.filter(uid = userid)
    # print(c)
    # print(c[0])
    # print(c[1])
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    n = len(c)
    summation = 0
    for x in c:
        # print(x)
        summation = summation + x.pid.price

    # print(summation)
    context = {}
    context['totalproducts'] = n
    context['total'] = summation
    context['products'] = c
    return render(request, 'cart.html', context)

def remove(request, cid):
    c = Cart.objects.filter(id = cid)
    c.delete()
    return redirect('/cart')

def removeFromPO(request, oid):
    o = Order.objects.filter(id = oid)
    o.delete()
    return redirect('/po')

def updateqty(request, qv, cid):
    # print(type(qv))
    # return HttpResponse("In Update Quantity")
    c = Cart.objects.filter(id = cid)
    # print(c)
    # print(c[0].qty)
    if qv == '1':
        t = c[0].qty + 1
        c.update(qty = t)
    else:
        if c[0].qty > 1:
            t = c[0].qty - 1
            c.update(qty = t)
    n = len(c)
    summation = 0
    for x in c:
        # print(x)
        summation = summation + x.pid.price * x.qty
    context = {}
    context['totalproducts'] = n * x.qty
    context['products'] = c
    context['total'] = summation
    # return HttpResponse("In Update Quantity")
    # return redirect('/cart')
    return render(request, 'cart.html', context)

def makepayment(request):
    orders = Order.objects.filter(uid = request.user.id)
    s = 0
    for x in orders:
        s = s + x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(auth=("rzp_test_pkOUV39BnpOhJM", "SDlz5aUE6Jk4ZDhwnifwQQzH"))

    data = { "amount": s * 100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data = data)
    print(payment)
    context = {}
    context['data'] = payment
    return render(request, 'pay.html', context)

def send_user_mail(request):
    uemail = request.user.email
    print(uemail)
    send_mail(
        "eStoreCart-Order Placed Successfully !!",
        "Order Placed Successfully and Payment Received.",
        "amazingsiddhesh@gmail.com",
        [uemail],
        fail_silently = False,
    )
    return HttpResponse("Mail is send successfully")

def about(request):
    # return HttpResponse("<h1>This is About Page.</h1>")
    return render(request, 'about.html')

def contact(request):
    # return HttpResponse("<b>This is Contact Page.</b>")
    return render (request, 'contact.html')

def addition(request, a, b):
    print(type(a))
    result = int(a) + int(b)
    return HttpResponse(result)

# Class Based Views

class SimpleView(View):
    def get(self, request):
        return HttpResponse("Hello from Simple View")



