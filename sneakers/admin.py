from django.contrib import admin
from .models import Product,Category,ProductImage,Contact,Cart,WishList,Subscription,Transaction,CustomerCart

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(CustomerCart)
admin.site.register(WishList)
admin.site.register(Subscription)
admin.site.register(Transaction)