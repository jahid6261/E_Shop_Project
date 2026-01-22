


from django.urls import path,include

from users.views import login_view,register_view,logout_view,profile


urlpatterns=[
    
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('profile/', profile, name="profile"),
    
]