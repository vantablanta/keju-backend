from django.urls import path
from .  import views



urlpatterns = [
    path('', views.endpoints, name='endpoints'), 
    path("products/", views.products, name='products'),
    path("add/", views.add, name='add'),
    path('categories/', views.categories, name='categories'),
    path('product_deals', views.product_deals, name ='deals'),


    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("signup/", views.signup, name='signup'),

]