from turtle import title
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
import jwt, datetime
import os
from apis.models import *
from apis.serializers import *
from pathlib import Path
from rest_framework import filters





from dotenv import load_dotenv
env_path = Path('.')/'.env'

load_dotenv(dotenv_path=env_path)
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


@api_view(['GET'])
def endpoints(request):
    api_urls = {
        "Signup": "/signup",
        "Login": "/login",
        "Categories": '/categories',
        "Add": "/add",
        "Deals" : '/deals',
        "Cart":"/cart/<str:pk>"
    }
    return Response(api_urls)

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    email = request.data['loginEmail']
    password = request.data['loginPassword']

    user = Users.objects.filter(email = email).first()

    if user is None:
        raise APIException("User not found")
       
    if not user.check_password(password):
        raise APIException("Incorrect Password!")

    payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
    }
        
    token = jwt.encode(payload, os.getenv('jwt_secret'), algorithm='HS256')

    response = Response()
    response.set_cookie(key='token', value=token, httponly=True)
    response.data = {
            'token':token,
    }
    return response


@csrf_exempt
@api_view(['GET', 'POST'])
def logout_user(request):
    response = Response()
    response.delete_cookie('token')
    response.data = {
        'message': 'Logout Successful'
        }
    return response

@csrf_exempt
@api_view(['POST'])
def signup(request):
    user_serializer = UsersModelSerializer(data = request.data)
    if user_serializer.is_valid():
        user_serializer.save()

        # email = user_serializer.data['email']
        # username = user_serializer.data['username']
        # signup_email(username,email)
            
        return Response(user_serializer.data)
    else:
        return Response(user_serializer.errors, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def get_user(request):  
    token = request.data['token']

    if not token:
        raise APIException('Unauthenticated')

    try:
        payload = jwt.decode(token, key=str(os.getenv('jwt_secret')), algorithms=['HS256'] )

    except jwt.ExpiredSignatureError: 
        raise APIException('Token expired')

    user = Users.objects.filter(id = payload["id"]).first()

    user_serializer = UsersModelSerializer(user)

    return Response(user_serializer.data)


@api_view(['GET'])
def products(request):
    products = Products.objects.all()
    product_serializer = ProductsModelSerializer(products, many=True)
    return Response(product_serializer.data)

@api_view(['GET'])
def product(request, pk):
    product = ProductDeals.objects.get(id = pk)
    product_serializer = ProductsModelSerializer(product, many=False)
    return Response(product_serializer.data)


@csrf_exempt
@api_view(['POST'])
def add(request):
        get_user(request)
        products_serializer = ProductsModelSerializer(data=request.data)
        if products_serializer.is_valid():
            products_serializer.save()
            return Response(products_serializer.data)
        else:
            return Response(products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def categories(request):
    categories = Categories.objects.all()
    categories_serializer = CategoriesModelSerializer(categories, many=True)
    return Response(categories_serializer.data)


@api_view(['GET'])
def single_category(request, pk):
    category = Categories.objects.get(id = pk)
    products = Products.objects.filter(category = category).all()
    products_serializer =  ProductsModelSerializer(products, many=True)
    return Response(products_serializer.data)


@api_view(['GET'])
def product_deals(request):
    deals =  ProductDeals.objects.all()
    deals_serializer = ProductDealsModelSerializer(deals, many = True)
    return Response(deals_serializer.data)


@api_view(['GET'])
def all_services(request):
    services = Services.objects.all()
    services_serializer = ServicesModelSerializer(services, many=True)
    return Response(services_serializer.data)


@api_view(['GET'])
def metaInfo(request):
    info = CompanyInfo.objects.all()
    info_serializer = ComapnyInfoModelSerializer(info, many = True)

    return Response(info_serializer.data)


@api_view(['GET'])
def popular_searches(request):
    searches = PopularSearches.objects.all()
    searches_serailizer =  PopularSearchesModelSerializer(searches, many = True )

    return Response(searches_serailizer.data)


@api_view(['GET'])
def get_cart(request):
    token = request.COOKIES.get('token')

    if not token:
        raise APIException('Unauthenticated')
    try:
        payload = jwt.decode(token, key=str(os.getenv('jwt_secret')), algorithms=['HS256'] )

    except jwt.ExpiredSignatureError: 
        raise APIException('Token expired')

    user = Users.objects.filter(id = payload["id"]).first()

    cart = Cart.objects.filter(buyer = user).all()
    cart_serializer = CartModelSerializer(cart, many=True)
    return Response(cart_serializer.data)


@csrf_exempt
@api_view(['POST'])
def add_to_cart(request, pk):
    # token = request.COOKIES.get('token')

    # if not token:
    #     raise APIException('Unauthenticated')
    # try:
    #     payload = jwt.decode(token, key=str(os.getenv('jwt_secret')), algorithms=['HS256'] )

    # except jwt.ExpiredSignatureError: 
    #     raise APIException('Token expired')

    username = request.data["username"]
    product_title = request.data['product_title']

    user = Users.objects.filter(username = username).first()
    products = ProductDeals.objects.get(title = product_title)

    cart = Cart.objects.create(buyer = user, products = products)
    cart.save()

    print(cart)

    return Response()


@api_view(['GET'])
def search(request):
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializer(queryset)
    return Response (serializer_class.data)
