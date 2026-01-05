from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from users.forms import RegistrationForm
# Create your views here.



def login_view(request):
    if request.method== "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "login succesfull")
            redirect("")
        else :
            messages.error(request,"invalid username or password") 
    return render(request,"")           


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Registration succesfull")
            return redirect ("")
    else :
        form = RegistrationForm()
    return render(request, "", {"form":form})    

def logout_view(request):
    logout(request) 
    return render("")

            