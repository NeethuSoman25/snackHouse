from django.db import models

# Create your models here.
class Client(models.Model):
  name=models.CharField(max_length=100)
  mobile=models.CharField(max_length=11)
  username=models.CharField(max_length=50)
  password=models.CharField(max_length=10)

  def __str__(self):
    return self.name

class Snacks(models.Model):
  food_image=models.ImageField(upload_to='pics')
  food_name=models.CharField(max_length=100)
  price=models.FloatField()

  def __str__(self):
    return self.food_name
  
class Tables(models.Model):
  table_name=models.CharField(max_length=4)
  quantity=models.IntegerField()

  def __str__(self):
    return self.table_name
  
class Order(models.Model):
  name=models.CharField(max_length=30)
  food_name=models.CharField(max_length=50)
  table_name=models.CharField(max_length=4)
  members=models.IntegerField(default=1)
  quantity=models.IntegerField(default=1)
  total_price=models.FloatField()

  def __str__(self):
    return self.name+"-"+self.food_name

class Payment(models.Model):
  name=models.CharField(max_length=30)
  total_amount=models.FloatField()

  def __str__(self):
    return self.name

class Contact(models.Model):
  name=models.CharField(max_length=40)
  username=models.CharField(max_length=40)
  message=models.TextField()

class Otp(models.Model):
  otp=models.IntegerField()
  email=models.CharField(max_length=100)

  def __str__(self):
    return self.email

  




