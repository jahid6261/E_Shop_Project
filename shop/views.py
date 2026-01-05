from django.shortcuts import render, get_object_or_404,redirect
from shop.models import Category, Product,Rating
from django.db.models import Q, Min, Max, Avg
from django.contrib import messages
from shop.forms import RatingForm

from order.models import Order,OrderItem


# home page

def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8] # descending order
    categories = Category.objects.all()
    
    return render(request, 'shop/home.html', {'featured_products' : featured_products, 'categories' : categories})

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    category = None
    
    
    if category_slug:
        category=get_object_or_404(category,category_slug)
        products=products.filter(category=category)
        
        
    min_price = products.aaggregate(Min("price"))['price__min']
    max_price=products.aaggregate(Max('price'))['price__max']
    
    if request.GET.get('min_price'):
        products=products.filter(price__gte=request.GET.get('min_price'))
    if request.GET.get('max_price')    :
        products=products.filter(price__gte=request.GET.get('max_price'))
        
        
    if request.GET.get('rating'):
     products=products.annotate(avg_rating=Avg("ratings__rating")).filter(
         
     avg_rating=request.GET.get("rating"
     ))  
    
    if request.GET.get("search"):
        queary=request.GET.get("search")
        products=products.filter(
            Q(name_icontains=queary)|
            Q(description_icontains=queary)|
            Q(category_name_icontains=queary)
            
        )
        
    return render(request,'',{
        'category': category,
        'categories':categories,
        'products':products,
        'min_price':min_price,
        'max_price':max_price
        
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
    
    return render(request, '', {
        'product' :product,
        'related_products' : related_products,
        'user_rating' : user_rating,
        'rating_form' : rating_form
    })




# rate product
def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    ordered_items = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__paid=True
    )

    if not ordered_items.exists():
        messages.warning(
            request,
            "You can only rate products you have purchased"
        )
        return redirect('product_detail', slug=product.slug)

    rating = Rating.objects.filter(
        product=product,
        user=request.user
    ).first()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            return redirect('product_detail', slug=product.slug)

    else:
        form = RatingForm(instance=rating)

    return render(
        request,
        '',
        {
            'form': form,
            'product': product
        }
    )

    