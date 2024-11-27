from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    age=models.IntegerField(null=True)
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=20)
    image=models.FileField(upload_to='image/',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Category(models.Model):
    categoryname=models.CharField(max_length=255)
    def _str_(self):
        return self.categoryname
    
class Product(models.Model):  
    productname=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.IntegerField(null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True) 
    image=models.FileField(upload_to='image/',null=True)
    def __str__(self):
        return self.productname

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.productname}"
    
   

    

    





