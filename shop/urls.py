from django.urls import path
from shop.views import product_list,product_detail,rate_product
urlpatterns=[
    
   
   path('products/', product_list, name="product_list"),
    path('products/<slug:category_slug>/', product_list, name="product_list_by_category"),
    path('products/detail/<slug:slug>/', product_detail, name="product_detail"),
    path('rate/<int:product_id>/', rate_product, name="rate_product"),
  
]