from django.shortcuts import render
from customer.forms import *
from renter.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
import json
from renter.forms import *
from rest_framework import generics
from .serializers import BrandSerializer, BikeSerializer
from django.shortcuts import redirect

# Create your views here.

def renter_home(request):
    un = request.session.get('username')
    if un:
        UO = User.objects.get(username=un)
        brands = Brand.objects.all()
        bikes = Bike.objects.all()
        d = {'UO': UO, 'brands': brands, 'bikes': bikes}
        return render(request, 'renter/renter_home.html', d)
    brands = Brand.objects.all()
    bikes = Bike.objects.all()
    d = {'brands': brands, 'bikes': bikes} 
    return render(request, 'renter/renter_home.html', d)

def renter_register(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    d = {'EUFO': EUFO, 'ECFO': EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MCFDO = PFDO.save(commit=False)
            MCFDO.username = MUFDO
            MUFDO.is_staff = True
            MUFDO.save()
            MCFDO.save()
            return HttpResponseRedirect(reverse('renter_home'))
        return HttpResponse('Invalid Data')
    return render(request, 'renter/renter_register.html', d)


def renter_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_active and AUO.is_staff:
            login(request, AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('renter_home'))
        return HttpResponse('Invalid Creds')

    return render(request, 'renter/renter_login.html')


def renter_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('renter_home'))

def renter_display_profile(request):
   un = request.session.get('username')
   UO = User.objects.get(username=un)
   PO = Profile.objects.get(username=UO)
   d = {'UO': UO, 'PO': PO}
   return render(request, 'renter/renter_display_profile.html', d)

def renter_forgetpw(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        UO = User.objects.get(username=un)
        if UO:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['username'] = un
            print(otp)
            return HttpResponseRedirect(reverse('renter_otp'))
    return render(request, 'renter/renter_forgetpw.html')

def renter_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gotp = request.session.get('otp')
        if int(otp) == gotp:
            return HttpResponseRedirect(reverse('newpw'))
        return HttpResponse('Invalid OTP')
    return render(request, 'renter/renter_otp.html')

def newpw(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            if UO:
                UO.set_password(pw)
                UO.save()
                return HttpResponseRedirect(reverse('renter_login'))
            return HttpResponse('Session Expired')
        return HttpResponse('Password Does Not Match')
    return render(request, 'renter/newpw.html')

def renter_changepw(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    if UO:
        otp = random.randint(100000, 999999)
        request.session['otp'] = otp
        request.session['username'] = un
        print(otp)
        return HttpResponseRedirect(reverse('renter_otp'))

def allbooking(request):
    status_filter = request.GET.get('status', '')  # Get ?status=Approved/Pending/Rejected

    if status_filter:
        allbookings = Booking.objects.filter(status=status_filter)
    else:
        allbookings = Booking.objects.all()

    context = {
        'allbookings': allbookings
    }
    return render(request, 'renter/allbooking.html', context)


def approve(request, pk):
    BO = Booking.objects.get(pk=pk)
    BO.status = 'Approve'
    BO.save()
    allbookings = Booking.objects.all()
    d = {'allbookings':allbookings}
    return render(request, 'renter/allbooking.html', d)
def reject(request, pk):
    BO = Booking.objects.get(pk=pk)
    BO.status = 'Reject'
    BO.save()
    allbookings = Booking.objects.all()
    d = {'allbookings':allbookings}
    return render(request, 'renter/allbooking.html', d)
    
def add_bikes(request):
    EBFO = BikeForm()
    d = {'EBFO': EBFO}
    if request.method == 'POST' and request.FILES:
        BFDO = BikeForm(request.POST, request.FILES)
        if BFDO.is_valid():
            BFDO.save()
            return HttpResponseRedirect(reverse('renter_home'))
    return render(request, 'renter/add_bikes.html', d)

def renter_display(request, brand):
    bikes = Bike.objects.filter(company=brand)
    d = {'bikes': bikes, 'brand': brand}
    return render(request, 'renter/renter_home.html', d)

def bike_map(request):
    """Display available bikes on Google Map"""
    bikes = Bike.objects.filter(is_available=True)
    bikes_data = [
        {
            "id": b.id,
            "name": b.bike_name,
            "brand": b.company.company,
            "price": b.price,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "image": b.photo.url if b.photo else "",
        }
        for b in bikes if b.latitude and b.longitude
    ]

    context = {
        'bikes_json': json.dumps(bikes_data)
    }
    return render(request, 'renter/bike_map.html', context)

#List all brands
class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
#List all bikes
class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    
#Single bike details
class BikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    
#List bikes by brand
class BikesByBrand(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        brand = self.kwargs['brand']
        return Bike.objects.filter(company__company=brand)

#List bikes by category
class BikesByCategory(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Bike.objects.filter(category=category)
    
#List bikes by availability
class BikesByAvailability(generics.ListAPIView):
    serializer_class = BikeSerializer

    def get_queryset(self):
        is_available = self.kwargs['is_available'].lower() == 'true'
        return Bike.objects.filter(is_available=is_available)