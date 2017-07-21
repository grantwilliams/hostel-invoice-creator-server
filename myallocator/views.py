from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from myallocator.models import Booking
from myallocator.serializers import BookingSerializer
import datetime

# Create your views here.
@api_view(['GET'])
@csrf_exempt
def search(request):
    query = request.GET['q']
    bookings = Booking.objects.filter(
        Q(first_name__istartswith=query) |
        Q(last_name__istartswith=query) |
        Q(email__istartswith=query) |
        Q(booking_id__istartswith=query)
    ).order_by('-arrival_date')

    serializer = BookingSerializer(bookings, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def fetch_all(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    serializer = BookingSerializer(bookings, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def fetch_booking(request):
    booking_id = request.GET['id']
    booking = Booking.objects.get(booking_id=booking_id)

    serializer = BookingSerializer(booking)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@csrf_exempt
def fetch_todays_arrivals(request):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    bookings = Booking.objects.filter(arrival_date=today).order_by('last_name')

    serializer = BookingSerializer(bookings, many=True)
    return JsonResponse(serializer.data, safe=False)
