from django.contrib import admin
from shop.models import Category,Product,Rating
# Register your models here.
admin.site.register(Category)




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','price','stock','available','created_at','updated_at']
    prepopulated_fields = {'slug': ('name',)}





admin.site.register(Rating)