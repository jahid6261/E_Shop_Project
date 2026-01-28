from order.models import Order
from django import forms


class CheckoutForm(forms.ModelForm)  :
    class Meta:
        model=Order      
        fields=['first_name','last_name','email','phone','address','postal_code','city','note']