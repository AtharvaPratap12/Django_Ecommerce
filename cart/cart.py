from store.models import Product,Profile
class Cart:
    def __init__(self,request):
        self.session = request.session
        self.request = request
        # Get the current session key if it exists.
        cart = self.session.get('session_key')


        

        # If the user is new, no session key!! Create One!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert {'3':1, '2':4} to {"3":1 , "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save the carty to the Profile Model
            current_user.update(old_cart = carty)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert {'3':1, '2':4} to {"3":1 , "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save the carty to the Profile Model
            current_user.update(old_cart = carty)

    def cart_total(self):
        # GET PRODUCT ID
        product_ids = self.cart.keys()
        # LOKK FOR THOSE KEY IN THE DICTIONARY/CART
        products = Product.objects.filter(id__in = product_ids)
        # Get Quantities
        quantities = self.cart
        # Start counting from 0 
        total = 0
        for key , value in quantities.items():
            # Convert the string into the int
            key = int(key)
            for product  in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total




    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from the cart
        product_ids = self.cart.keys()
        # use ids to lookup products in the database models
        product = Product.objects.filter(id__in = product_ids)
        # Reurn those lookup products
        return product

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get the cart
        ourcart =  self.cart
        # Update the cart or dictionary
        ourcart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert {'3':1, '2':4} to {"3":1 , "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save the carty to the Profile Model
            current_user.update(old_cart = carty)

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        #Delete from dictionary/Cart
        if product_id  in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert {'3':1, '2':4} to {"3":1 , "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save the carty to the Profile Model
            current_user.update(old_cart = carty)