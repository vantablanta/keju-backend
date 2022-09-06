from rest_framework import serializers 
from .models import Categories, ProductDeals, Products, Users
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class ProductsModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Products
        fields = '__all__'

class UsersModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'password do not match'})
        user.set_password(password)
        user.save()
        return user



class CategoriesModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categories
        fields = '__all__'
class ProductDealsModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductDeals
        fields = '__all__'

