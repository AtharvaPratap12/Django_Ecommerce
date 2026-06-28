from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms

# Create your views here.
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