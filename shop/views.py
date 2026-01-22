from django.shortcuts import render, get_object_or_404,redirect
from shop.models import Category, Product,Rating
from django.db.models import Q, Min, Max, Avg
from django.contrib import messages
from shop.forms import RatingForm

from order.models import Order,OrderItem

from django.contrib.auth.decorators import login_required




# product list page
def product_list(request, category_slug = None):
    category = None 
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        print("category .......", category)
        products = products.filter(category = category)
        
    min_price = products.aggregate(Min('price'))['price__min']
    max_price = products.aggregate(Max('price'))['price__max']
    
    if request.GET.get('min_price'):
        products = products.filter(price__gte=request.GET.get('min_price'))
    
    if request.GET.get('max_price'):
        products = products.filter(price__lte=request.GET.get('max_price'))
    
    if request.GET.get('rating'):
        min_rating = request.GET.get('rating')
        products = products.annotate(avg_rating = Avg('ratings__rating')).filter(avg_rating__gte=min_rating)
        # temp variable --> avg_rating
        # Avg
        # ratings related_name ke use kore rating model er rating value ke access korlam
        # avg_rating == user er filter kora rating er sathe
        
    
    if request.GET.get('search'):
        query = request.GET.get('search')
        products = products.filter(
            Q(name__icontains = query) | 
            Q(description__icontains = query) | 
            Q(category__name__icontains = query)  
        )
    
    return render(request, 'product_list.html', {
        'category' : category,
        'categories' : categories,
        'products' : products,
        'min_price' : min_price,
        'max_price' : max_price
    })

# product detail page
def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug, available = True)
    related_products = Product.objects.filter(category = product.category).exclude(id=product.id)
    
    user_rating = None 
    
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(product=product, user=request.user)
        except Rating.DoesNotExist:
            pass 
        
    rating_form = RatingForm(instance=user_rating)
    
    return render(request, 'product_detail.html', {
        'product' :product,
        'related_products' : related_products,
        'user_rating' : user_rating,
        'rating_form' : rating_form
    })

# Rate Product 
# logged in user, Purchase koreche kina
@login_required
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    ordered_items = OrderItem.objects.filter(
        order__user = request.user,
        product = product,
        order__paid = True
    )
    
    if not ordered_items.exists(): # order kore nai
        messages.warning(request, 'You can only rate products you have purchased!')
        return redirect('product_detail', slug=product.slug)
    
    try:
        rating = Rating.objects.get(product=product, user = request.user)
    except Rating.DoesNotExist:
        rating = None 
    
    # jodi rating age diye thake tail rating form ager rating data diye fill up kora thakbe sekhtre instance = user rating hoye jbe
    # jodi rating na kora thake taile instance = None thakbe and se new rating create korte parbe
    if request.method == 'POST':
        form = RatingForm(request.POST, instance = rating) 
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user 
            rating.save()
            return redirect('product_detail', slug=product.slug)
    else:
        form = RatingForm(instance=rating)
    
    return render(request, 'rate_product.html', {
        'form' : form,
        'product' : product
    })
    