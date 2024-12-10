from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .models import Client,Snacks,Tables,Order,Payment,Contact,Otp
import random
from django.core.mail import send_mail
from django.conf import settings

def index(request):
  return render(request,'nouser.html')

def about(request):
  return render(request,'about.html')

def contact(request):
  if request.method=='POST':
     name=request.POST['name']
     username=request.POST['username']
     message=request.POST['message']
     newcontact=Contact(name=name,username=username,message=message)
     newcontact.save()
     messages.info(request,'Message is saved,our staff will contact you shortly')
  return render(request,'contact.html')

def login_page(request):
  return render(request,'login.html')

def register_page(request):
  if request.method == 'POST':
     name=request.POST['name']
     mobile=request.POST['mobile']
     username=request.POST['username']
     password1=request.POST['password1']
     password2=request.POST['password2']
     if password1==password2:
        if User.objects.filter(username=username).exists():
           messages.info(request,'email has been taken')
        else:
           user=User.objects.create_user(username=username,password=password1,first_name=name)
           client=Client(name=name,mobile=mobile,username=username,password=password1)
           code=generate_code()
           newOtp=Otp(otp=code,email=username)
           newOtp.save()
           user.save()
           client.save()
           send_email(username,code)
           messages.info(request,'otp send to your given mail')
           login(request,user)
           return redirect('otpPage')
     else:
        messages.info(request,'password not match')
        return redirect('register')
  return render(request, 'register.html')

def login_view(request):
   if request.method == 'POST':
      username=request.POST['username']
      password=request.POST['password']
      user=authenticate(username=username,password=password)
      if user is not None:
         login(request,user)
         
         return render(request, 'home.html')
      else:
         message='invalid credentials'
         messages.info(request,message)
   return render(request, 'login.html')

def logout_view(request):
   logout(request)
   messages.info(request,'Logged out successfully')
   return redirect('index')

def home(request):
   return render(request,'home.html')

def habout(request):
   return render(request,'habout.html')

def hcontact(request):
   if request.method=='POST':
     name=request.POST['name']
     username=request.POST['username']
     message=request.POST['message']
     newcontact=Contact(name=name,username=username,message=message)
     newcontact.save()
     messages.info(request,'Message is saved,our staff will contact you shortly')
   return render(request,'hcontact.html')

def food(request):
   foods=Snacks.objects.all()
   return render(request,'food.html',{'foods':foods})

def order(request):
   food_name=request.POST['foodname']
   price=request.POST['price']
   tables=Tables.objects.all()
   return render(request,'order.html',{'tables':tables,'food':food_name,'price':price})

def orderFood(request):
   name=request.POST['fname']
   food_name=request.POST['foodname']
   table=request.POST['table']
   members=request.POST['members']
   members=int(members)
   quantity=request.POST['quantity']
   price=request.POST['tprice']
   if table=='none':
      messages.info(request,'Choose a table to continue')
      return HttpResponseRedirect(reverse('food'))
   elif checkorder(table,food_name,name):
      if Order.objects.filter(name=name,table_name=table).exists(): 
         checktable(request,name,table,members,food_name,price,quantity)
         return HttpResponseRedirect(reverse('ordertable'))
      else:
         if Order.objects.filter(table_name=table).exists():
            messages.info(request,'This table is already reserved by other')
            return HttpResponseRedirect(reverse('food'))
         else:
            checktable(request,name,table,members,food_name,price,quantity)
            return HttpResponseRedirect(reverse('food'))
   else:
      messages.info(request,'You had already booked this item for the table')
      return HttpResponseRedirect(reverse('food'))

def ordertable(request):
   
      tables=Tables.objects.all()
      name = request.user.first_name

        
      if Order.objects.filter(name=name).exists():
         orders = Order.objects.filter(name=name)
            
      else:
         orders = 'none'

        
      return render(request, 'order.html', {'details': orders,'tables':tables})
  
       
         
"""
   name=request.user.first_name
   if Order.objects.filter(name=name).exists():
      orders=Order.objects.filter(name=name)
   else:
      orders='none'
   return render(request,'ordertable.html',{'details':orders})"""

def payment(request):
      fname=request.POST['fname']
      userorder=Order.objects.filter(name=fname).values_list('total_price',flat=True)
      userorder=list(userorder)
      amount=0
      for order in userorder:
         amount=order+amount
         newPayment=Payment(name=fname,total_amount=amount)
      newPayment.save()
      return HttpResponseRedirect(reverse('confirm'))

def orderdetails(request):
   name=request.user.first_name
   order=Order.objects.filter(name=name)
   client=Client.objects.filter(name=name)
   payments=Payment.objects.filter(name=name)
   random_num=random.randint(10000,99999)
   return render(request,'order_details.html',{'orders':order,'clients':client
                                               ,'payments':payments,'rand':random_num})

def confirmMessage(request):
   name=request.user.first_name
   userpayment=Payment.objects.filter(name=name)
   return render(request,'payment_alert.html',{'payments':userpayment})

def cancelOrder(request):
   name=request.user.first_name
   food=request.POST['food']
   table=request.POST['table']
   order=Order.objects.filter(name=name,food_name=food,table_name=table)
   order.delete()
   messages.info(request,'order cancelled')
   return HttpResponseRedirect(reverse('ordertable'))

def cancelPayment(request):
   name=request.user.first_name
   payment=Payment.objects.filter(name=name)
   payment.delete()
   messages.info(request,'payment cancelled')
   return HttpResponseRedirect(reverse('ordertable'))

def confirmPayment(request):
   name=request.user.first_name
   payment=Payment.objects.filter(name=name)
   order=Order.objects.filter(name=name)
   payment.delete()
   order.delete()
   messages.info(request,'paid successfully')
   return HttpResponseRedirect(reverse('home'))

def updateOrder(request):
   name=request.user.first_name
   food=request.POST['food1']
   table=request.POST['table1']
   foodprice=Snacks.objects.filter(food_name=food)
   order=Order.objects.filter(name=name,food_name=food,table_name=table)
   return render(request,'updateorder.html',{'updorder':order,'prices':foodprice})

def updateorderfood(request):
   name=request.user.first_name
   food_name=request.POST['foodname']
   table=request.POST['table']
   members=request.POST['members']
   members=int(members)
   quantity=request.POST['quantity']
   price=request.POST['tprice']
   checktable(request,name,table,members,food_name,price,quantity)
   return HttpResponseRedirect(reverse('ordertable'))

def otpPage(request):
   if request.method == 'POST':
      otp=request.POST['otp']
      otp=int(otp)
      email=request.POST['mail']
      details=Otp.objects.get(email=email)
      generateOtp=details.otp
      if otp==generateOtp:
         details.delete()
         messages.info(request,'successfully registered')
         return render(request,'home.html')
      else :
         messages.info(request,'invalid otp')
   return render(request,'otp.html')

#--------------------------------------------------Helper functions------------------------------------------------------------------
def checkorder(table,food,name):
   order=Order.objects.filter(table_name=table,food_name=food,name=name)
   if order.exists():
      return False
   else:
      return True
   
def checktable(request,name,table,members,food,price,quantity):
   table_quantity=Tables.objects.filter(table_name=table).values_list('quantity',flat=True)
   for tabquant in table_quantity:
      tabquant=int(tabquant)
      if members<=tabquant:
         totalprice=float(price)*int(quantity)
         oldorder=Order.objects.filter(name=name,food_name=food,table_name=table)
         oldorder.delete()
         updateorder=Order(name=name,food_name=food,table_name=table,members=members
                           ,quantity=quantity,total_price=totalprice)
         updateorder.save()
         messages.info(request,'order successfully')
      else:
         messages.info(request,'Members are higher than the reserved seat')

def send_email(email,otp):
   otp=str(otp)
   send_mail(
            'VERIFICATION CODE',
            'Your otp for this session:- AC-'+otp,
            settings.EMAIL_HOST_USER,  
            [email],
            fail_silently=False
        )

def generate_code():
   code=random.randint(1000,9999)
   return code