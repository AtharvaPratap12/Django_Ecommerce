from .cart import Cart

# Create context processors so it can work on all the webpage

def cart(request):
    # Return the default data from our cart
    return {'cart': Cart(request)}