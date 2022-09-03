from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('',views.HomePage,name="home"),
    path('product/<str:pk>/',views.ProductPage,name="product"),
    path('cart',views.Carts,name="cart"),
    path('edit-cart/<str:pk>/',views.editCarts,name="edit-cart"),
    path('delete-cart/<str:pk>/',views.deleteCart,name="delete-cart"),
    path('wishlist/<str:pk>/',views.wishList,name="wishlist"),
    path('contact/',views.Contacts,name="contact"),
    path('transaction/', views.TranscationPage, name="transaction"),
    path('create-checkout-session', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('payment-cancel/', views.paymentCancel, name='payment-cancel'),
    path('webhook/stripe',views.my_webhook_view, name='webhook-stripe')
]