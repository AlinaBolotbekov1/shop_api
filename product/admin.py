from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.register(Category)
# admin.site.register(Product)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['slug', 'title']
#     list_filter = ['title', 'price']
#     search_fields = ['title', 'description']


# admin.site.register(Product, ProductAdmin)

from review.models import Comment

class CommentInline(admin.TabularInline):
    model = Comment

class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Product, ProductAdmin)

