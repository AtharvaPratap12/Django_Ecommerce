from django.db import models
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    phone = models.CharField(max_length = 15)
    address = models.TextField(max_length = 500)
    password = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.CharField(max_length = 500, blank = True, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 1)
    image = models.ImageField(upload_to = 'uploads/products/')
    # Add a new thing 
    is_sale = models.BooleanField(default = False)
    sale_price = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    address = models.CharField(max_length = 500, default = '', blank = True, null = True)
    phione = models.CharField(max_length = 15, default = '', blank = True, null = True)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.product.name
