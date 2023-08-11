from django.db import models

# Create your models here.


class signintable(models.Model):
    fname = models.CharField(max_length=200)
    Lname = models.CharField(max_length=200)
    Uname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class adminregistertable(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class addingproducttable(models.Model):
    productname = models.CharField(max_length=200)
    productprice = models.CharField(max_length=200)
    productcatagory = models.CharField(max_length=200)
    productdescription = models.CharField(max_length=200)
    productimage=models.ImageField(upload_to="productimage/")
    productsize=models.CharField(max_length=200)

class carttable(models.Model):
    items_id = models.ForeignKey(addingproducttable, on_delete=models.CASCADE)
    user_id = models.ForeignKey(signintable, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(max_length=200)
    status = models.CharField(max_length=200, default='pending')


