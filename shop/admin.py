from django.contrib import admin
from shop.models import Category, Product, Rating, ProductImage

# Category
admin.site.register(Category)

# Rating
admin.site.register(Rating)

# ProductImage Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]  
