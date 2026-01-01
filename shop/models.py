from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


# CATEGORY MODLES

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    description= models.TextField()
    
    class Meta:
        verbose_name_plural="Categories"
        
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=250,unique=True)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,
    related_name="products") 
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)   
    stock=models.PositiveBigIntegerField(default=1)
    available= models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='products/%Y/%M/%D')
    
    def __str__(self):
        return self.name
    
    
    
    def average_ratings(self):
        ratings= self.ratings.all()
        if ratings.count() > 0:
            return sum([i.ratting for i in ratings ])/ratings.count()
class Rating(models.Model):
    Product=models.ForeignKey(Product,on_delete=models.CASCADE,
    related_name='ratings')   
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveBigIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} -{self.Product.name}-{self.rating}"
    
    
    
    
    
    
        
    
    
    
    