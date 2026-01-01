from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

# Create your models here.



class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    
class CartItem(models.Model) :
    cart =models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.quantity} X{self.product.name}"
    def get_cost(self):
        return self.quantity*self.product.price
    
    
class Order(models.Model):
        STATUS=[
            ('pending','Pending'),
            ('processing','Processing'),
            ('shiped','Shiped'),
            ('delivered','Delivered'),
            ('canceled','Canceled'),
        ]
        
        user= models.ForeignKey(User,on_delete=models.CASCADE,
                                related_name='orders')
        first_name=models.CharField(max_length=100)
        last_name=models.CharField(max_length=100)
        email_name=models.EmailField(max_length=100)     
        address=models.TextField(max_length=100)
        postal_code=models.CharField(max_length=100)
        city=models.CharField(max_length=100) 
        note=models.TextField()
        paid=models.BooleanField(default=False)
        transaction_id=models.CharField(max_length=100)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        statud=models.CharField(max_length=10,choices=STATUS)
        
        
        def __str__(self):
         return f"order #{self.id}"    
        def get_total_cost(self):
            return sum(item.get_cost() for item in self.items.all())
    
        
class OrderItem(models.Model):
    
    order=models.ForeignKey(Order,on_delete=models.CASCADE,
                            related_name='order_items')   
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def get_cost(self):
        return self.quantity*self.product.price
    

        
        

        
        
        
        