from django.db import models
from django.urls import reverse
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    
    class Meta:
        #admin 노출 시 표기
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']
        db_table = 'Category'

    # 상세페이지 
    def get_absolute_url(self):
        return reverse('store:categoty_list', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    title_image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_author')
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'images/%Y.%m.%d', blank=True, null=True) 

    #PositiveIntegerField 음수를 받지 않는다.
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255, db_index=True, unique=True, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL , null=True, related_name='products')
    display = models.BooleanField('Display', default=True)
    order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
        db_table = 'Product'
        #병합해 index 산출
        index_together = [['id','slug']]


    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.title