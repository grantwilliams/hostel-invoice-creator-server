from django.db import models

# Create your models here.
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=30)
    channel = models.CharField(max_length=10)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    arrival_date = models.DateField()
    departure_date = models.DateField()
    nights = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    pax = models.IntegerField()
    room_names = models.CharField(max_length=50)
    total_price = models.FloatField()
    deposit = models.FloatField()

    objects = models.Manager()
