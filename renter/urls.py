from django.urls import path
from renter.views import *

urlpatterns = [
    path('', renter_home, name='renter_home'),
    path('renter_register/', renter_register, name='renter_register'),
    path('renter_login/', renter_login, name='renter_login'),
    path('renter_logout/', renter_logout, name='renter_logout'),
    path('renter_display_profile/',  renter_display_profile, name='renter_display_profile'),
    path('renter_forgetpw/', renter_forgetpw, name='renter_forgetpw'),
    path('renter_otp/', renter_otp, name='renter_otp'),
    path('newpw/', newpw, name='newpw'),
    path('renter_changepw/', renter_changepw, name='renter_changepw'),
    path('renter_display<brand>', renter_display, name='renter_display'),
    path('allbooking/', allbooking, name ='allbooking'),
    path('approve<pk>', approve, name='approve'),
    path('reject<pk>', reject, name='reject'),
    path('add_bikes/', add_bikes, name='add_bikes'),
    path('brands/', BrandList.as_view(), name='brand-list'),
    path('bikes/', BikeList.as_view(), name='bike-list'),
    path('bikes/<int:pk>/', BikeDetail.as_view(), name='bike-detail'),
    path('map/', bike_map, name='bike_map'),
    # filter by brand (example: /renter/bikes/brand/Honda/)
    path('bikes/brand/<str:brand>/', BikesByBrand.as_view(), name='bikes-by-brand'),
     # filter by category (example: /renter/bikes/category/Scooter/)
    path('bikes/category/<str:category>/', BikesByCategory.as_view(), name='bikes-by-category'),
     # filter by availability (example: /renter/bikes/availability/true/)
    path('bikes/availability/<str:is_available>/', BikesByAvailability.as_view(), name='bikes-by-availability'),
]
