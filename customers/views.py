from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import RegisterForm, EditAccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# variable page name is telling django the Name of our site and logo
global pageName, pageLogo
pageName = "Footcap"
pageLogo = "/static/images/logo.svg"


def RegisterPage(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'pageName':pageName, 'pagelogo':pageLogo, 'form':form}
    return render(request, 'customers/register.html',context)


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password'].lower()

        try:
            user = User.objects.get(username=username)
        except:
            print("Username is invalid")

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            print("Login Successful")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            print("An error occur")

    context = {'pageName':pageName, 'pagelogo':pageLogo }
    return render(request, 'customers/login.html',context)


@login_required(login_url="login")
def Account(request):
    customer = request.user.register

    # total quantity
    carts_list_count = customer.cart_set.exclude(status="paid").values_list('quantity')
    cart_count = []
    for raw_count_carts in carts_list_count:
        for count_cart in raw_count_carts:
            cart_count.append(count_cart)
    total_cart = sum(cart_count)

    wishlist = customer.wishlist_set.all()

    context = {'customer':customer, 'pagelogo':pageLogo, 'pageName':pageName, 'total_cart':total_cart,
               'wishlists':wishlist}
    return render(request, 'customers/account.html',context)

@login_required(login_url="login")
def editAccount(request):
    customer = request.user.register

    # total quantity
    carts_list_count = customer.cart_set.exclude(status="paid").values_list('quantity')
    cart_count = []
    for raw_count_carts in carts_list_count:
        for count_cart in raw_count_carts:
            cart_count.append(count_cart)
    total_cart = sum(cart_count)

    form = EditAccountForm(instance=customer)
    if request.method == 'POST':
        form = EditAccountForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            if len(str(customer.contact)) > 10 or len(str(customer.contact)) < 10:
                print("incorrect phone number")
            else:
                customer.save()
                return redirect('account')

    context = {'customer':customer, 'pagelogo':pageLogo, 'pageName':pageName, 'form':form, 'total_cart':total_cart}
    return render(request, 'customers/edit-account.html',context)


@login_required(login_url="login")
def deletePage(request,pk):
    customer = request.user.register
    wishlist = customer.wishlist_set.get(id=pk)
    if request.method == 'POST':
        wishlist.delete()
        return redirect('account')
    context = {'obj':wishlist, 'pagelogo':pageLogo, 'pageName':pageName}
    return render(request, 'delete.html',context)








