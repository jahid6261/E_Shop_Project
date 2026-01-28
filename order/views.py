from django.shortcuts import render,redirect,get_object_or_404

from shop.models import Product
from django.contrib import messages

from order.forms import CheckoutForm
from django.contrib.auth.decorators import login_required



from order.models import Order,OrderItem,Cart,CartItem
from order.sslcommerz import generate_sslcommerz_payment
from order.sslcommerz import send_order_confirmation_email

from django.views.decorators.csrf import csrf_exempt






@login_required
def cart_detail(request):
   
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    return render(request, 'cart.html', {'cart' : cart})

# cart add
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try: 
        cart = Cart.objects.get(user=request.user)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        

    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity = 1)
    
    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect('product_detail', slug=product.slug)
    


@login_required
def cart_update(request, product_id):
 
    
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    quantity = int(request.POST.get('quantity', 1))
    

    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, f"{product.name} has been removed from your cart!")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Cart updated successfully!!")
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    cart_item.delete()
    messages.success(request, f"{product.name} has been removed from your cart!")
    return redirect("cart_detail")



# Product --> Cart Item --> Order Item
@csrf_exempt 
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart_detail')
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_detail')
    
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) 
            order.user = request.user 
            order.phone = form.cleaned_data['phone']
            order.save() 

            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product, 
                    price = item.product.price, 
                    quantity = item.quantity 
                )
      
            
            request.session['order_id'] = order.id 
            return redirect('payment_process')
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {
        'cart' : cart,
        'form' : form
    })



    







@csrf_exempt

def payment_success(request, order_id):
    order = get_object_or_404(Order, id= order_id)
    
    order.paid = True 
    order.status = 'processing'
    order.transaction_id = order.id 
    order.save()
    order_items = order.order_items.all()
    for item in order_items:
        product = item.product
        product.stock -= item.quantity
        
   
        if product.stock < 0:
            product.stock = 0
        product.save()
    
 
    send_order_confirmation_email(order)
    
    messages.success(request, 'Payment successful')
    return render(request, 'payment_success.html', {'order' : order})


@csrf_exempt
def payment_process(request):

    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id)
    payment_data = generate_sslcommerz_payment(request, order)
    
 
    if payment_data.get('status') == 'SUCCESS' and payment_data.get('GatewayPageURL'):
        return redirect(payment_data['GatewayPageURL'])
    else:
        print("Payment Data:", payment_data)  
        messages.error(request, 'Payment gateway error. Please Try again.')
        return redirect('checkout')



@csrf_exempt

def payment_fail(request, order_id):
    order = get_object_or_404(Order, id= order_id, user=request.user)
    order.status = 'canceled'
    order.save()
    return redirect('checkout')


@csrf_exempt
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id= order_id, user=request.user)
    order.status = 'canceled'
    order.save()
    return redirect('cart_detail')