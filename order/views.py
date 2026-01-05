from django.shortcuts import render,redirect,get_object_or_404

from shop.models import Product
from django.contrib import messages

from order.forms import CheckoutForm

from .import sslcommerz



from order.models import Cart,CartItem,Order,OrderItem
# Create your views here.



def cart_add(request,product_id):
    
    product= get_object_or_404(Product,id=product_id)
    
    try:
        cart=Cart.objects.get(user=request.user)
        
    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=request.user)  
        
    try :
        cart_item=CartItem.objects.get(cart=cart,product=product)
        cart_item.quantity +=1
        cart_item.save()
        
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart,product=product,quantity=1) 
    
    
    messages.success(request,f'{product.name} has been added to your cart')  
    
    return redirect(request,'')          



# cart update

def cart_update(request,product_id):
    
    cart =get_object_or_404(Cart,user=request.user)
    product=get_object_or_404(Product,product_id)
    cart_item=get_object_or_404(CartItem, cart=cart,product=product)
    
    
    quantity=int(request.POST.get('quantity',1))  
    
    if quantity <=0:
        cart_item.delete()
        messages.success(request,f'{product.name}has been deleted from you cart')  
    else :
        cart_item.quantity=quantity
        cart_item.save()
        messages.success(request,f'cart updated sunccesfully')  
        
        return redirect(redirect,'')  
    
    
def cart_remove(request,product_id)    :
    cart=get_object_or_404(Cart,user=request.user)
    product=get_object_or_404(Product,id=product_id)
    cart_item=get_object_or_404(CartItem,cart=cart)
    
    cart_item.delete()
    
    messages.success(request,f'{product.name} has been deleted from your cart')
    
    return redirect('')




def cart_detail(request):
    
    try:
       
       cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
       cart=Cart.objects.create(user=request.user)  
       return render (request,'',{'cart':cart})
   
   
   
def checkout(request)  :
    
    try :
        cart=Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request,'your cart is emspy')
            return redirect('')
        
    except Cart.DoesNotExist:
        messages.warning(request,'your cart is empty')
        return redirect("")
    
    if request.method=="POST":
        form=CheckoutForm(request.POST)
        
        if form.is_valid():
            order=form.save(commit=False)
            order_user=request.user
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart.items.all().delete() # cart er item gula delete kore dilam 
            request.session['order_id'] = order.id 
            return redirect('')
    else:
        form = CheckoutForm()
    return render(request, '', {
        'cart' : cart,
        'form' : form
    })
    
    



