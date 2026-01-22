from django.urls import path

from order.views import cart_detail,checkout,cart_add,cart_remove,cart_update,payment_cancel,payment_process,payment_fail,payment_success

urlpatterns=[
    
    path('cart/',cart_detail, name='cart_detail'),
    path('checkout/', checkout, name="checkout"),
    path('cart/add/<int:product_id>/',cart_add, name="cart_add"),
    path('cart/remove/<int:product_id>/', cart_remove, name="cart_remove"),
    path('cart/update/<int:product_id>/', cart_update, name="cart_update"),
    
    
    path('payment/process/', payment_process, name="payment_process"),
    path('payment/success/<int:order_id>/', payment_success, name="payment_success"),
    path('payment/fail/<int:order_id>/',payment_fail, name="payment_fail"),
    path('payment/cancel/<int:order_id>/', payment_cancel, name="payment_cancel"),
]