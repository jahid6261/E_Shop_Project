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
    # user er kono cart nai
    # user er cart ache
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    return render(request, 'cart.html', {'cart' : cart})


# cart add
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # User er cart ache kina
    
    # Exception handling
    # jodi thake taile oi cart ta check korbo
    try: # ekahne error aste pare
        cart = Cart.objects.get(user=request.user)
    
    # jodi na thake, taile cart ekta banabo
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    # Cart e item add korbo
    # item already cart e ache
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        
    # item cart e nai
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity = 1)
    
    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect('product_detail', slug=product.slug)






# cart Update
# cart item quantity increase/decrease korte parbo
@login_required
def cart_update(request, product_id):
    # cart konta
    # cart er item konta
    # main product jeta cart item hisebe cart e ache
    
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Keya saban -> stock e ache 20 ta product
    # user Keya saban -> 40 ta add to cart korche..
    # user Keya saban -> 5, 4, 3, 2, 1, 0 --> cartitem delete kore deoya lagbe
    
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




    





#@csrf_exempt # --> payment related kaj gula jeno secure thake setar jonne  
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
    
    # Checkout form ta fill up korbe
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # form object create hobe kintu data database e jabe na
            order.user = request.user 
            order.save() # order kora hoye geche

            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product, # cartitem e ekhn order item
                    price = item.product.price, # product er main price e order item er main price
                    quantity = item.quantity # cart item er quantity e hocche order item er quantity
                )
            #  order kora done finally
            # cart er ar kono value e nai
            cart.items.all().delete() # cart er item gula delete kore dilam 
            request.session['order_id'] = order.id 
            return redirect('payment_process')
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {
        'cart' : cart,
        'form' : form
    })

# 1. Payment Success
@csrf_exempt

def payment_success(request, order_id):
    order = get_object_or_404(Order, id= order_id)
    # order ta paid
    # order er status --> processing
    # product er stock komiye dibo
    # transaction id
    order.paid = True 
    order.status = 'processing'
    order.transaction_id = order.id 
    order.save()
    order_items = order.order_items.all()
    for item in order_items:
        product = item.product
        product.stock -= item.quantity
        
        # 40 - 60 = -20
        if product.stock < 0:
            product.stock = 0
        product.save()
    
    # send confirmation email
    send_order_confirmation_email(order)
    
    messages.success(request, 'Payment successful')
    return render(request, 'payment_success.html', {'order' : order})

@csrf_exempt
def payment_process(request):
    # session 
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id)
    payment_data = generate_sslcommerz_payment(request, order)
    
    if payment_data['status'] == 'SUCCESS':
        return redirect(payment_data['GatewayPageURL'])
    else:
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