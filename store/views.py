from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # Get the thing from Db
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(category__name__icontains = searched))
        # Test for null
        if not searched:
            messages.success(request, "The product is not there Plss try again later!!!!!!")
            return render(request, 'search.html', {})
        
        else:
            return render(request, 'search.html', {'searched':searched})

    else:
        return render(request, 'search.html', {})





def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id = request.user.id)
        # Get Current user Shipping Address
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        # Get original user form
        form = UserInfoForm(request.POST or None, instance = current_user )
        # get users shipping form
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user )

        if form.is_valid() or shipping_form.is_valid() :
            form.save()
            shipping_form.save()
            messages.success(request, "The User Info  has been been Updated!!!!!!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:

            messages.error(request, 'You must be logged in to access the page')
            return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # If they filled out the Form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the Form Valid
            if form.is_valid():
                form.save()
                messages.success(request, "Youu have successfully changed the password u have to login again")
                return redirect('login')
            else:
                for error in list (form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html',{'form': form})

    else:
        messages.success(request, 'You must be logged in to see that page ')
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user )

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "The User has been been Updated!!!!!!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:

            messages.error(request, 'You must be logged in to access the page')
            return redirect('home')

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

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id) 
            # Get there saved cart from the database.
            saved_cart = current_user.old_cart
            # Convert the database string to python dictinary
            if saved_cart:
                # Convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to session
                # get the cart
                cart = Cart(request)
                # Loop through the cart and add the items from the database

                for key,value in converted_cart.items():
                    cart.db_add(product = key, quantity = value)




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
            messages.success(request, "User has been registered successfully. Please update your user information below")
            return redirect('update_info')
        else:
            messages.success(request, "OOPS!!! Something went wrong. Please try again...")
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})