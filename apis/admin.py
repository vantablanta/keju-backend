from django.contrib import admin
from  .models import *
# Register your models here.


admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(ProductDeals)
admin.site.register(Services)
admin.site.register(CompanyInfo)
admin.site.register(PopularSearches)
admin.site.register(Cart)