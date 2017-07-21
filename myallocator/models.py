from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.
class Booking(models.Model):
    booking_id = models.CharField(primary_key=True, max_length=30)
    channel = models.CharField(max_length=5)
    booking_date = models.DateField()
    arrival_date = models.DateField()
    departure_date = models.DateField()
    nights = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    pax = models.IntegerField()
    room_names = ArrayField(models.CharField(max_length=50))
    total_price = models.FloatField()
    deposit = models.FloatField()

    objects = models.Manager()

    def dates_list(self):
        return [(self.arrival_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(self.nights)]
