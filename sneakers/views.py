from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import Product, Category, ProductImage, Register, Cart, Contact, WishList, Subscription,CustomerCart
from django.db.models import Q
from .utils import searchEngine
from .forms import CartForm, SubscriptionForm, TransactionForm
from django.contrib.auth.decorators import login_required

# variable page name is telling django the Name of our site and logo
global pageName, pageLogo
pageName = "Footcap"
pageLogo = "/static/images/logo.svg"


def HomePage(request):
    products, search_products = searchEngine(request)
    brands = Product.objects.all().values_list('product_brand', flat=True).distinct()
    conpanies = []
    for company in brands:
        conpanies.append(company)
    brands_set = set(conpanies)
    brand_list = list(brands_set)
    brands = brand_list[0:5]
    form = SubscriptionForm()
    try:
        customer = request.user.register
    except:
        customer = None
    total_cart = 0
    # total quantity
    if customer:
        carts_list_count = customer.cart_set.exclude(status="paid").values_list('quantity')
        cart_count = []
        for raw_count_carts in carts_list_count:
            for count_cart in raw_count_carts:
                cart_count.append(count_cart)
        total_cart = sum(cart_count)

        # total price
        product_prices = customer.cart_set.exclude(status="paid").values_list('total_price')
        total_prices = []
        for raw_price in product_prices:
            for price in raw_price:
                total_prices.append(price)
        total = sum(total_prices)
    else:
        total = 0


    try:
        subscribers = Subscription.objects.get(username=customer)
        subscriber = True
    except:
        subscriber = False

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.username = customer
            subscriber.save()
            return redirect('home')

    context = {'pageName': pageName, 'pagelogo': pageLogo, 'form':form , 'brands':brands, 'subscribers':subscriber,
               'search':
        search_products,
               'products': products, 'total_cart':total_cart, 'total':total}
    return render(request, 'sneakers/home.html', context)


def ProductPage(request, pk):
    # get logged in user ingo
    try:
        customer = request.user.register
    except:
        customer = None

    # get form for carting
    form = CartForm()

    # get the product details from product model through id
    product = Product.objects.get(id=pk)
    related_products = Product.objects.exclude(id=pk)
    otherimages = ProductImage.objects.filter(product_title=product.id)

    # total quantity
    try:
        carts_list_count = customer.cart_set.exclude(status="paid").values_list('quantity')
        cart_count = []
        for raw_count_carts in carts_list_count:
            for count_cart in raw_count_carts:
                cart_count.append(count_cart)
        total_cart = sum(cart_count)
    except:
        total_cart = 0


    # checks if logged in customer have carted the product before
    try:
        cart = customer.cart_set.exclude(status='paid').get(product_name=product)
    except:
        cart = None


    # I wrote this to do : if a customer has carted a product this will collect only all the id of customers that has
    # carted this product and check if the current logged in custer id exists in it to if it exists it will tell the
    # customer to edit order

    carted = Cart.objects.filter(product_name=product).exclude(status="paid").values_list('customer_id', flat=True)

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart = form.save(commit=False)

            # check if there is no  more quantity then tells the customer no more quantity
            if cart.quantity == 0:
                print('Not allowed')
            else:
                price = product.product_price * cart.quantity
                cart.user = customer
                cart.customer_id = customer.id
                cart.product_name = product
                cart.total_price = price

                # if ordered quantity is greater than quantity available
                if product.product_quantity < cart.quantity:
                    print("no product allowed")
                else:
                    cart.save()
                    # this code subtracts ordered quantity from original product quantity
                    product.product_quantity = product.product_quantity - cart.quantity
                    product.save()
                    return redirect('home')

    context = {'pageName': pageName, 'pagelogo': pageLogo, 'form': form, 'product': product,
               'related_products': related_products, 'otherimages': otherimages, 'cart': cart,
               'customer': customer,
               'total_cart': total_cart, 'carted': carted}
    return render(request, 'sneakers/single-product.html', context)




@login_required(login_url="login")
def Carts(request):
    customer = request.user.register
    carts = customer.cart_set.exclude(status="paid")

    # total quantity
    carts_list_count = carts.values_list('quantity')
    cart_count = []
    for raw_carts in carts_list_count:
        for cart in raw_carts:
            cart_count.append(cart)
    total_cart = sum(cart_count)

    # total price
    product_prices = customer.cart_set.exclude(status="paid").values_list('total_price')
    total_prices = []
    for raw_price in product_prices:
        for price in raw_price:
            total_prices.append(price)
    total = sum(total_prices)
    context = {'pageName': pageName, 'pagelogo': pageLogo, 'total': total, 'carts': carts, 'total_cart': total_cart}
    return render(request, 'sneakers/cart.html', context)


@login_required(login_url="login")
def editCarts(request, pk):
    page_url = 'edit-Cart'
    customer = request.user.register
    product = Cart.objects.get(id=pk)
    products = Product.objects.get(id=product.product_name.id)
    related_products = Product.objects.exclude(id=pk)
    otherimages = ProductImage.objects.filter(product_title=product.product_name)

    cart = customer.cart_set.get(id=pk)
    update_product_qauntity = products.product_quantity + cart.quantity
    pq = update_product_qauntity
    form = CartForm(instance=cart)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            editcart = form.save(commit=False)
            if editcart.quantity > pq:
                print("invalid process")
            else:
                price = products.product_price * editcart.quantity
                editcart.total_price = price
                products.product_quantity = pq - editcart.quantity
                products.save()
                editcart.save()
                return redirect('cart')

    context = {'pageName': pageName, 'pq': pq, 'product': product, 'form': form, 'related_products': related_products,
               'otherimages': otherimages, 'page_url': page_url}
    return render(request, 'sneakers/single-product.html', context)


@login_required(login_url="login")
def deleteCart(request, pk):
    try:
        page_url = 'Delete'
        customer = request.user.register
        cart = customer.cart_set.get(id=pk)
        products = Product.objects.get(id=cart.product_name.id)

        if request.method == 'POST':
            products.product_quantity = products.product_quantity + cart.quantity
            products.save()
            cart.delete()
            return redirect('cart')
    except:
        return redirect('home')
    context = {'pageName': pageName, 'obj': cart, 'page_url': page_url, 'pagelogo':pageLogo}
    return render(request, 'sneakers/delete.html', context)


@login_required(login_url="login")
def wishList(request,pk):
    customer = request.user.register
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        wishlist = WishList.objects.create(
            user=customer,
            customer_id=customer.id,
            product_id=product.id,
            wishlist_product=product
        )
        wishlist.save()
        return redirect('home')
    context = {'obj':product, 'pageName': pageName, 'pagelogo':pageLogo}
    return render(request, 'sneakers/wishlist_confirm.html',context)



def Contacts(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        contact = Contact.objects.create(
            name=name,
            email=email,
            subject = "customer contact",
            body=message
        )
        contact.save()
        return redirect('home')
    context = {}
    return render(request, 'sneakers/contact.html')


@login_required(login_url='login')
def TranscationPage(request):

    customer = request.user.register
    carts = customer.cart_set.exclude(status="paid")
    if carts:
        pass
    else:
        return redirect('home')
    cart = Cart.objects.filter(user=customer)

    form = TransactionForm()

    #solution
    """
    create another table for order then have a special column called orderItem then
    it should be a many to many relationship
    """

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transact = form.save(commit=False)
            transact.username = customer
            transact.save()
            for customer_cart in cart:
                customer_cart.status = 'paid'
                customer_cart.save()
            return redirect('home')
    context = {'form':form, 'carts':carts}
    return render(request, 'sneakers/payment_method.html', context)





def logoutPage(request):
    logout(request)
    return redirect('login')























