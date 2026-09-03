from django.db import models
from django.contrib.auth.models import User

# # Create your models here.

# class Mini(models.Model):
#     product_image=models.ImageField(upload_to='miniature')
#     product_name=models.CharField(max_length=120)
#     product_sex=models.CharField(max_length=130,null=True,blank=True)
#     product_price=models.IntegerField()
#     product_dprice=models.IntegerField()
#     def _str_(self):
#         return self.product_name
    
# class Newarrivals(models.Model):
#     newproduct_image=models.ImageField(upload_to='newarrivals')
#     newproduct_name=models.CharField(max_length=120,)
#     newproduct_price=models.IntegerField()
#     newproduct_dprice=models.IntegerField()
#     def _str_(self):
#         return self.newproduct_name
    
# class Bestsellers(models.Model):
#     bestproduct_image=models.ImageField(upload_to='bestsellers')
#     bestproduct_name=models.CharField(max_length=120)
#     bestproduct_price=models.IntegerField()
#     bestproduct_dprice=models.IntegerField()
#     def _str_(self):
#         return self.bestproduct_name
    
#class Community(models.Model):
#     image=models.ImageField(upload_to='Comunity')
 #    video=models.FileField(upload_to='Community')
  #   name=models.CharField(max_length=120)
   #  price=models.IntegerField()
    # def _str_(self):
      #   return self.name


class Category(models.Model):
    name= models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    genter=models.CharField(max_length=130,null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    dprice=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='products')
    video=models.FileField(upload_to='products' ,blank=True ,null=True)
    ML=models.IntegerField(null=True,blank=True)
    details=models.CharField(max_length=200, blank=True)
    notes=models.CharField(max_length=200, blank=True)
    season=models.CharField(max_length=200,blank=True)
    occasion=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)

class Cartitem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.product.dprice * self.quantity

    class Meta:
        unique_together = ('cart', 'product') 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    location = models.CharField(max_length=100, blank=True)
    pincode=models.DecimalField(max_digits=7,blank=True,null=True,decimal_places=0)
    state=models.CharField(max_length=20,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=True ,blank=True)
    phone = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'product')