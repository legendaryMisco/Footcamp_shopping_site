from .models import Product,Category,ProductImage,Register
from django.db.models import Q


def searchEngine(request):
    search_products = ''
    if request.GET.get('search'):
        search_products = request.GET.get('search')
    else:
        search_products = ''

    categories = Category.objects.filter(product_category__icontains=search_products)

    products = Product.objects.distinct().filter(
        Q(product_title__icontains=search_products) |
        Q(product_description__icontains=search_products) |
        Q(product_price__icontains=search_products) |
        Q(product_category__in=categories)
    )
    return products,search_products
