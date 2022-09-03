from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterPage, name="register"),
    path('login/', views.LoginPage, name="login"),
    path('', views.Account, name="account"),
    path('edit-account/',views.editAccount,name="edit-account"),
    path('delete/<str:pk>/',views.deletePage,name="delete"),
    path('logout/', views.logoutPage, name="logout"),
]











