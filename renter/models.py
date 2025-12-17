from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Brand(models.Model):
    company = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.company
    

class Bike(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'Road Bike 🚴'),
        ('mountain', 'Mountain Bike ⛰️'),
        ('electric', 'Electric Bike ⚡'),
    ]
    company = models.ForeignKey(Brand, on_delete=models.CASCADE)
    bike_name = models.CharField(max_length=50)
    desc = models.TextField()
    photo = models.ImageField(upload_to='bike_photos')
    
    price = models.CharField(max_length=10)
    rating = models.FloatField(default=0)
    
    is_available = models.BooleanField(default=True)                          # availability filter
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="road")  # category filter
    bookings_count = models.PositiveIntegerField(default=0)                   # popularity filter
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} {self.bike_name}"
    
class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    bike_name = models.ForeignKey(Bike, on_delete=models.CASCADE,related_name='images')
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_date = models.DateField(auto_now=False, auto_now_add=False)    
    pickup_time = models.TimeField(auto_now=False, auto_now_add=False)
    drop_date = models.DateField(auto_now=False, auto_now_add=False)
    drop_time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50, default='Pending')


    def __str__(self):
        return f"Booking {self.booking_id} - {self.username} ({self.bike_name})"

