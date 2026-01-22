# core/views.py
from django.shortcuts import render
from shop.models import Product, Category  # shop এর model import করতে হবে

def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'home.html', {'featured_products': featured_products, 'categories': categories})

