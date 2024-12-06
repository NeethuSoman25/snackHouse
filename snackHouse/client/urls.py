from django.urls import path
from . import views
urlpatterns=[
  path('',views.index,name='index'),
  path('about',views.about,name='about'),
  path('contact',views.contact,name='contact'),
  path('register/', views.register_page, name='register'),
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),
  path('home',views.home,name='home'),
  path('home/about',views.habout,name='habout'),
  path('home/contact',views.hcontact,name='hcontact'),
  path('home/snacks',views.food,name='food'),
  path('home/order',views.order,name='order'),
  path('home/orderfood',views.orderFood,name='orderFood'),
  path('home/ordertable',views.ordertable,name='ordertable'),
  path('home/payment',views.payment,name='payment'),
  path('home/orderdetails',views.orderdetails,name='orderdetails'),
  path('home/confirm',views.confirmMessage,name='confirm'),
  path('home/cancelorder',views.cancelOrder,name='cancelorder'),
  path('home/cancelpay',views.cancelPayment,name='cancelpay'),
  path('home/updateorder',views.updateOrder,name='updateorder'),
  path('home/updateorderfood',views.updateorderfood,name='updateorderfood'),
  path('home/confirmpay',views.confirmPayment,name='confirmpay'),
  path('otp',views.otpPage,name='otpPage')
]