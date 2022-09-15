from django.urls import path
from .  import views



urlpatterns = [
    path('', views.endpoints, name='endpoints'), 
    path("products/", views.products, name='products'),
    path("add/", views.add, name='add'),
    path('categories/', views.categories, name='categories'),
    path('product_category/<str:pk>', views.single_category, name='category'),
    path('product_deals/', views.product_deals, name ='deals'),
    path('services/', views.all_services, name ='services'),
    path('info/', views.metaInfo, name="info" ), 
    path('popular_searches/', views.popular_searches, name="searches" ), 
    path("product/<str:pk>", views.product, name='product'),
    path('search/', views.search, name='search'),

    path("login/", views.login_user, name='login'),
    path('profile/', views.get_user, name="user"),
    path('add_to_cart/<str:pk>', views.add_to_cart, name="add_to_art"),
    path('get_cart/', views.get_cart, name="get_cart"),
    path("logout/", views.logout_user, name='logout'),
    path("signup/", views.signup, name='signup'),

]