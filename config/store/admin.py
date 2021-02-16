from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    #카테고리 등록시 필드 자동으로 만들어줌
    prepopulated_fields = {'slug':['name']}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug', 'title_image', 'category','price','order', 'quantity', 'display','image','created','updated']
    list_filter = ['display','created','category']
    prepopulated_fields = {'slug': ['title']}
    #편집을 쉽게 도와줌
    list_editable = ['price','quantity','display','order']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)




