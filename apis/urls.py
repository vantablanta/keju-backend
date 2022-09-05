from django.urls import path
from .  import views


urlpatterns = [
    path('', views.endpoints, name='endpoints'), 
    path("products/", views.products, name='products'),
    path("add/", views.add, name='add'),
    path("cart/<str:pk>/", views.add_to_cart, name='cart'),

    path("login/", views.login_user, name='login'),
    path("signup/", views.signup, name='signup'),
]