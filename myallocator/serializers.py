from rest_framework import serializers
from myallocator.models import Booking

class BookingSerializer(serializers.Serializer):
    booking_id = serializers.CharField(max_length=30, read_only=True)
    channel = serializers.CharField(max_length=5)
    booking_date = serializers.DateField()
    booking_time = serializers.TimeField()
    arrival_date = serializers.DateField()
    departure_date = serializers.DateField()
    nights = serializers.IntegerField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    pax = serializers.IntegerField()
    room_names = serializers.ListField()
    total_price = serializers.FloatField()
    deposit = serializers.FloatField()
    dates = serializers.ListField(source='dates_list')
