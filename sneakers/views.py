from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.db.models import Q
from .utils import searchEngine
from .forms import CartForm, SubscriptionForm, BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# variable page name is telling django the Name of our site and logo
global pageName, pageLogo
pageName = "Footcap"
pageLogo = "/static/images/logo.svg"

def HomePage(request):
    products, search_products = searchEngine(request)
    products_list = Product.objects.all().order_by('-created')[:8]
    top_list = Product.objects.all().order_by('-product_price')[:3]
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
            messages.success(request, f"""{customer} you have subscribed to {pageName}.. you will get updates on latest
                                     products""")
            return redirect('home')

    context = {'pageName': pageName, 'pagelogo': pageLogo, 'product_list':products_list, 'top_list':top_list,
               'form':form , 'brands':brands,
               'subscribers':subscriber,
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
                messages.error(request,f"""This Product is not available.. subscribe to {pageName} to get notification 
                                       when product is available or contact us """)
            else:
                price = product.product_price * cart.quantity
                cart.user = customer
                cart.customer_id = customer.id
                cart.product_name = product
                cart.total_price = price

                # if ordered quantity is greater than quantity available
                if product.product_quantity < cart.quantity:
                    messages.error(request,"""Opps demanded quantity not available right now try demand less or 
                    contact us """)
                else:
                    cart.save()
                    # this code subtracts ordered quantity from original product quantity
                    product.product_quantity = product.product_quantity - cart.quantity
                    product.save()
                    messages.success(request, f'{product} have been added to cart successfully')
                    return redirect('home')

    context = {'pageName': pageName, 'pagelogo': pageLogo, 'form': form, 'product': product,
               'related_products': related_products, 'otherimages': otherimages, 'cart': cart,
               'customer': customer,
               'total_cart': total_cart, 'carted': carted}
    return render(request, 'sneakers/single-product.html', context)




@login_required(login_url="login")
def Carts(request):
    customer = request.user.register
    form = BillingForm()
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

    billing_address_checker = customer.cart_set.exclude(status="paid").values_list('billings_id', flat=True)

    billing_address = BillingAddress.objects.all().values_list('id',flat=True)

    is_billingAddress = False

    for billing_id in billing_address_checker:
        if billing_id in list(billing_address):
            is_billingAddress = True
        else:
            is_billingAddress = False

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.username = customer
            billing.customer_id = customer.id
            for customer_cart in carts:
                customer_cart.billings_id\
                    =billing.id
                customer_cart.save()
            billing.save()

    context = {'pageName': pageName,
               'pagelogo': pageLogo,
               'customer':customer, 'form':form,
               'total': total, 'carts': carts,
               'total_cart':total_cart,
               'existing_billing':billing_address_checker, 'billing':billing_address, 'is_billing':is_billingAddress}
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
                messages.error(request, """Opps demanded quantity not available right now try demand less or 
                                    contact us """)
            else:
                price = products.product_price * editcart.quantity
                editcart.total_price = price
                products.product_quantity = pq - editcart.quantity
                products.save()
                editcart.save()
                messages.success(request, f""" {product.product_name} in cart list was updated successfully """)
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
            messages.success(request, f'{products} deleted from cart ')
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
        messages.success(request, f"""{product} have been added to wishlist""")
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
        messages.success(request, f'We have received your message {name} we will response to you very soon ')
        return redirect('home')
    context = {}
    return render(request, 'sneakers/contact.html')

# for payment
import stripe
from django.conf import settings
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

class CreateCheckoutSessionView(generic.View):
    def post(self, *args ,  **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        customer_id = self.request.POST.get('order-id')
        carts = Cart.objects.filter(customer_id=customer_id).exclude(status="paid")

        # total price
        product_prices = carts.values_list('total_price')
        total_prices = []
        for raw_price in product_prices:
            for price in raw_price:
                total_prices.append(price)
        total = sum(total_prices)
        carts_total_price = (round(total) * 0.0024) * 100
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': round(carts_total_price),
                        'product_data' : {
                            'name': 'Footcamp orders'
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= YOUR_DOMAIN +'payment-success/',
            cancel_url= YOUR_DOMAIN + 'payment-success/',
        )
        return redirect(checkout_session.url, code=303)


def paymentSuccess(request):
    customer = request.user.register
    carts = customer.cart_set.exclude(status="paid")
    if carts:
        pass
    else:
        return redirect('home')
    cart = Cart.objects.filter(user=customer)

    # solution
    """
    create another table for order then have a special column called orderItem then
    it should be a many to many relationship
    """
    for customer_cart in cart:
        customer_cart.status = 'paid'
        customer_cart.save()
        messages.success(request, 'order purchased successfully')
    return redirect('home')


def paymentCancel(request):
    context = {
        'payment_status' : 'cancel'
    }
    return render(request, 'sneakers/confirmation.html',context)

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == "paid":
            fulfill_order()

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order():
    pass

def TranscationPage(request):

    customer = request.user.register
    carts = customer.cart_set.exclude(status="paid")
    if carts:
        pass
    else:
        return redirect('home')
    cart = Cart.objects.filter(user=customer)



    #solution
    """
    create another table for order then have a special column called orderItem then
    it should be a many to many relationship
    """
    for customer_cart in cart:
        customer_cart.status = 'paid'
        customer_cart.save()
        messages.success(request, 'order purchased successfully')
    return redirect('home')





























