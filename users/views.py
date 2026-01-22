from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from order.models import Order

from users.forms import RegistrationForm
# Create your views here.



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successful!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password") 
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created! Please check your email to verify your account."
            )
            return redirect('login')  
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def profile(request):
    tab = request.GET.get('tab')
    orders = Order.objects.filter(user = request.user)
    completed_orders = orders.filter(status = 'delivered')
    total_spent = sum(order.get_total_cost() for order in orders)
    order_history_active = (tab == 'orders') # true or false return korbe
    
    return render(request, 'profile.html', {
        'user' : request.user,
        'orders' : orders,
        'completed_orders' : completed_orders,
        'total_spent' : total_spent,
        'order_history_active' : order_history_active
    })
            