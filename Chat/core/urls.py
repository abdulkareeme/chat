from django.urls import path
from . import  views
from knox.views import LogoutView


urlpatterns = [
    path('login', views.login_api, name='login_api'),
    path('user_info', views.user_info, name='user_info'),
    path('register', views.register_api, name='register_api'),
    path('logout',LogoutView.as_view() , name='logout'),
    path('users',views.ListUser.as_view(), name='users_list')
]