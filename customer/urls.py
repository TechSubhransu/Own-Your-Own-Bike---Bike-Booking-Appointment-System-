from django.urls import path
from customer.views import *
urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('display_profile/', display_profile, name='display_profile'),
    path('forgetpw/', forgetpw, name='forgetpw'),
    path('otp/', otp, name='otp'),
    path('newpw/', newpw, name='newpw'),
    path('changepw/', changepw, name='changepw'),
    path('display<brand>', display, name='display'),
    path('book<pk>', book, name='book'),
    path('search', search, name='search'),
    path('show<pk>', show, name='show'),
    path('my_bookings', my_bookings, name='my_bookings'),
]