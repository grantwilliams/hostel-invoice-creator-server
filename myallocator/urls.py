from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^search/all/$', views.fetch_all, name='search_all'),
    url(r'^search/today/$', views.fetch_todays_arrivals, name='fetch_today'),
    url(r'^booking/$', views.fetch_booking, name="fetch_booking"),
    url(r'^booking/add/', views.add_booking, name="add_booking")
]
