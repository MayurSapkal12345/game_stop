from django.shortcuts import render, HttpResponse, redirect
from gamestopapp.models import product, cart, orders, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import random


# Create your views here.
def home(request):
  
  return render(request, 'landing.html')


def index(request):
    
    return render(request, 'index.html')

def create_product(request):
    
    if request.method == "GET":
    
      return render(request, 'createproduct.html')
  
    else:
        
        name = request.POST['name']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']
        
        p = product.objects.create(name=name, description=description, manufacturer=manufacturer, category=category, price=price, image=image)
        
        p.save()
        
        return redirect('/')
      

def read_product(request):
  
  if request.method == "GET":
  
     p = product.objects.all()
     
     context = {}
     
     context['data'] = p
  
     return render(request, 'readproduct.html', context)
  
  else:
    name = request.POST['search']
    
    prod = product.objects.get(name = name)
    
    return redirect(f"read_product_detail/{prod.id}")
   

def update_product(request, rid):
  
  if request.method == "GET":
    
      p = product.objects.filter(id = rid)
        
      context = {}
    
      context['data'] = p
    
      return render(request, 'updateproduct.html', context)
    
  else:
        
        name = request.POST['uname']
        description = request.POST['udescription']
        manufacturer = request.POST['umanufacturer']
        category = request.POST['Ucategory']
        price = request.POST['uprice']
        
        p = product.objects.filter(id = rid)
        
        p.update(name=name, description=description, manufacturer=manufacturer, category=category, price=price)
        
        
        return redirect('/readproduct')
      

def delete_product(request, rid):
  
    p = product.objects.filter(id = rid)
    
    p.delete()
    
    return redirect('/readproduct')
  
  

def user_register(request):
  
  if request.method == "GET":
    
    return render(request, 'register.html')
  
  else:
    
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    if password == confirm_password:
      
      u = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
      
      u.set_password(password)
      
      u.save()
      
      return redirect('/login')
    
    else:
      
      context = {}
      
      context['error'] = "password and confirm_password are not match"
      
      return render(request, 'register.html', context)
    
    

def user_login(request):
  
  if request.method == "GET":
    
    return render(request, 'login.html')
  
  else:
    
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
      
      login(request, user)
      
      return redirect('/')
    
    else:
      
      context = {}
      
      context['error'] = "username and password incorect"
      
      return render(request, 'login.html', context)
    
    
def user_logout(request):
  
  logout(request)
  
  
  return redirect('/')


@login_required(login_url="/login")
def create_cart(request, rid):
  
  prod = product.objects.get(id = rid)
  
  Cart = cart.objects.filter(product = prod, user=request.user).exists()
  
  if Cart:
    
      return redirect('/readcart')
  
  else:
  
    user = User.objects.get(username = request.user)
  
    total_price = prod.price
  
    c = cart.objects.create(product = prod, user=user, quantity=1, total_price=total_price)
  
    c.save()
  
    return redirect('/readcart')



@login_required(login_url= "/login")
def read_cart(request):
  
  c = cart.objects.filter(user = request.user)
  
  context = {}
  
  context['data'] = c
  
  total_quantity = 0
  total_price = 0
  
  for x in c:
    
    total_quantity += x.quantity
    total_price += x.total_price
    
    context['total_quantity'] = total_quantity
    context['total_price'] = total_price
    
  
  return render(request, 'readcart.html', context)


def delete_cart(request, rid):
  
  Cart = cart.objects.filter(id = rid)
  
  Cart.delete()
  
  return redirect('/readcart')


def update_cart(request, rid, q):
  
  Cart = cart.objects.filter(id = rid)
  
  c = cart.objects.get(id = rid)
  
  print(q)
  
  quantity = int(q)
  price = int(c.product.price) * quantity
  
  Cart.update(quantity = q, total_price=price)
  
  return redirect('/readcart')


def create_orders(request, rid):
  
  Cart = cart.objects.get(id = rid)
  
  order = orders.objects.create(product = Cart.product, user = request.user, quantity = Cart.quantity, total_price = Cart.total_price)
  
  order.save()
  
  Cart.delete()
  
  return redirect('/readcart')


def read_orders(request):
  
  order = orders.objects.filter(user = request.user)
  
  context = {}
  
  context['data'] = order
  
  return render(request, 'readorder.html', context)


def create_review(request, rid):
  
  prod = product.objects.get(id = rid)
  
  rev = Review.objects.filter(user = request.user, product=prod).exists()
  
  if rev:
    
    return HttpResponse("Review already added")
  
  else:
    if request.method == "GET":
  
      return render(request, 'createreview.html')
  
    else:
    
      title = request.POST['title']
      content = request.POST['content']
      rating = request.POST['rate']
      image = request.FILES['image']
      
      prod = product.objects.get(id = rid)
      
      review = Review.objects.create(product=prod, user=request.user, title=title, content=content, rating=rating, image=image)
      
      review.save()
      
      return HttpResponse("review added")


def read_product_detail(request, rid):
  
  prod = product.objects.filter(id = rid)
  
  p = product.objects.get(id = rid)
  
  n = Review.objects.filter(product = p).count()
  
  rev = Review.objects.filter(product = p)
  
  sum = 0
  
  for x in rev:
  
    sum += x.rating
  
  try:
    
    avg_r = sum/n
    avg = int(sum/n)
  
  except:
    print("No review")
    
    context = {}
    
    context['data'] = prod
    
    if n == 0:
      
      context['avg'] = "no review"
    
    else:
    
     context['avg_rating'] = avg
     context['avg'] = avg_r
   
  
  return render(request, 'readproductdetail.html', context)


def foregot_password(request):
  
  if request.method == "GET":
    
    return render(request, 'forgotpassword.html')
  
  else:
    
    email = request.POST['email']
    
    #*
    request.session['email'] = email
    
    user = User.objects.filter(email = email).exists()
    
    if user:
      
      otp = random.randint(1000, 9999)
      request.session['otp'] = otp
      
      with get_connection(
        
        host = settings.EMAIL_HOST,
        port = settings.EMAIL_PORT,
        username = settings.EMAIL_HOST_USER,
        password = settings.EMAIL_HOST_PASSWORD,
        use_tls = settings.EMAIL_USE_TLS
        
        
      ) as connection :
        
        subject = "OTP Verification"
        email_from = settings.EMAIL_HOST_USER
        reciption_list = [ email ]
        message = f"OTP is {otp}"
        
        EmailMessage(subject, message, email_from, reciption_list, connection = connection).send()
      
      return redirect('/otp_verification')
    
    else:
      
      context = {}
      
      context['error'] = "user does not exist"
      
      return render(request, 'forgotpassword.html', context)
      
  
  
def otp_verification(request):
  
  if request.method == "GET":
    
  
    return render(request, 'otp.html')
  
  else:
    
    otp = int(request.POST['otp'])
    
    email_otp = int(request.session['otp'])
    
    if otp == email_otp:
      
      return redirect('/new_password')
    
    else:
      
      return HttpResponse("not ok")


def new_password(request):
  
  if request.method == "GET":
  
    return render(request, 'newpassword.html')
  
  else:
    email = request.session['email']
    
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    user = User.objects.get(email = email)
    
    if password == confirm_password:
      
      user.set_password(password)
      
      user.save()
      
      return redirect('/login')
    
    else:
      
      context = {}
      
      context['error'] = "password and confirm_password are not match"
      
      return render(request, 'newpassword.html', context)




  
  
  






      
    
    
    
  
  
      







