from django.db import models
import uuid
from customers.models import Register
# Create your models here.


class Product(models.Model):
   id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
   product_image = models.ImageField(max_length=3000, default='logo.svg', upload_to='products/')
   product_title = models.CharField(max_length=300, null=False, blank=False)
   product_price = models.DecimalField(max_digits=10,decimal_places=2,null=False,blank=False)
   product_description = models.TextField(null=True,blank=True)
   product_quantity = models.BigIntegerField(default=0,null=False,blank=False)
   product_category = models.ManyToManyField('Category')
   product_brand = models.CharField(max_length=300,null=False,blank=False)
   created = models.DateTimeField(auto_now_add=True)




   class Meta:
       ordering = ['created']

   def __str__(self):
       return self.product_title




class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    product_title = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    product_image = models.ImageField(max_length=3000, upload_to='products/', null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_title)


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    product_category = models.CharField(max_length=50,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_category


class Contact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=300, null=False, blank=False)
    body = models.TextField( null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    customer_id = models.UUIDField(null=True, blank=True)
    product_name = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.BigIntegerField(null=False,blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default="unpaid",null=False,blank=False)
    billings_id = models.UUIDField(
        editable=True, null=True, blank=True)
    transaction_id = models.OneToOneField('Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.status


# class CustomerCart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
#     user = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
#     customer_id = models.UUIDField(null=True, blank=True)
#     product_name = models.ManyToManyField(Cart)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     status = models.CharField(max_length=20, default="unpaid",null=False,blank=False)
#     transaction_id = models.OneToOneField('Transaction', on_delete=models.SET_NULL, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.status


class WishList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    customer_id = models.UUIDField(null=True, blank=True)
    wishlist_product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.UUIDField(null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.wishlist_product)


class Subscription(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    username = models.CharField(max_length=300,null=True,blank=True)
    email = models.EmailField(max_length=3000,null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class BillingAddress(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,
                          unique=True,
                          editable=False)
    username = models.ForeignKey(Register,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    fullname = models.CharField(max_length=300,
                                null=False,
                                blank=False)
    email = models.EmailField(max_length=500,
                              null=False,
                              blank=False)
    address = models.CharField(max_length=500,
                               null=False,
                               blank=False)
    city = models.CharField(max_length=300,
                            null=False,
                            blank=False)
    state = models.CharField(max_length=30,
                             null=False,
                             blank=False)
    zip_code = models.IntegerField(null=False,
                                   blank=False)

    customer_id = models.UUIDField(null=True,
                                   blank=True)
    created = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.fullname
class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    username = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,blank=True)
    transaction_items = models.TextField(
        null=True,blank=True)
    customer_id = models.UUIDField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_items






