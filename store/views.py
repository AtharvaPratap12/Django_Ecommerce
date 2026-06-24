from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', { 'categories': categories })



def category(request, foo):
    #Replace hyphens with spaces 
    foo = foo.replace('-', ' ')
    # Grab the category from the url and filter products based on that category
    try:
        category = Category.objects.get(name = foo)
        product = Product.objects.filter(category  = category)
        return render(request, 'category.html', {'products': product, 'category': category})
    except:
        messages.error(request, "No Category found with the name " + foo  + ". Please try again.")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in succesfully!!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!!!!")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have been registered successfully!!!")
            return redirect('login')
        else:
            messages.success(request, "OOPS!!! Something went wrong. Please try again...")
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})