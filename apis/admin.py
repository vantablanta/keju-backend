from django.contrib import admin
from  .models import Users, Products, Categories, ProductDeals
# Register your models here.


admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(ProductDeals)