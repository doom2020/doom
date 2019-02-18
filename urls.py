from django.urls import path

from .views import *

urlpatterns = [
    path('', main_views, name='main'),
    path('firm_show/', firm_show_views, name='firm_show'),
    path('cooperation/', cooperation_views, name='cooperation'),
    path('employment/', employment_views, name='employment'),
    path('contact-me', contact_me_views, name='contact'),
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('register/', register_views, name='register'),
    path('goods_detail/<int:gtype>/<int:page>', goods_detail_views, name='goods_detail'),
    path('goods_detail_one/<str:goods_name>', goods_detail_one_views, name='goods_detail_one'),
    path('order/', order_views, name='order'),
    path('user_info/', user_info_views, name='user_info'),
    path('check_register/', check_register_views, name='check_register'),
    path('add_address/', add_address_views, name='add_address'),
    path('update_shopping_car/', update_shopping_car_views, name='update_shopping_car'),
]