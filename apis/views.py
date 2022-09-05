from itertools import product
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
import jwt, datetime
import os
from apis.models import Products, Users, Cart
from apis.serializers import ProductsModelSerializer, UsersModelSerializer
from pathlib import Path
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .emails import signup_email
from django.shortcuts import get_object_or_404


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
        "Products": '/products',
        "Add": "/add",
        "Cart":"/cart/<str: pk>"
    }
    return Response(api_urls)


@csrf_exempt
@api_view(['GET', 'POST'])
def login_user(request):
    email = request.data['email']
    password = request.data['password']

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
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
            'token':token
    }
    return response


@csrf_exempt
@api_view(['POST', 'GET'])
def signup(request):
    user_serializer = UsersModelSerializer(data = request.data)
    if user_serializer.is_valid():
        user_serializer.save()

        email = user_serializer.data['email']
        username = user_serializer.data['username']
        signup_email(username,email)
            
        return Response(user_serializer.data)
    else:
        return Response(user_serializer.errors, status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(['GET'])
def get_user(request):
    token = request.COOKIES.get('jwt')

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


@csrf_exempt
@api_view(['POST'])
def add(request):
    products_serializer = ProductsModelSerializer(data=request.data)
    if products_serializer.is_valid():
        products_serializer.save()
        return Response(products_serializer.data)
    else:
        return Response(products_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def add_to_cart(request, pk):
    if request.user.is_authenticated:
        try:
            item = get_object_or_404(Products, pk)
            cart = Cart.objects.create(buyer = request.user, product=item)
            cart.save()
        except ObjectDoesNotExist:
            pass
    else:
        return Response("You need to be logged in ")