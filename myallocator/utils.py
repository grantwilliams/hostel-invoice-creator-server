import os
import csv
from datetime import datetime
import mechanicalsoup
import requests.exceptions
from celery.utils.log import get_task_logger
from myallocator.models import Booking

def download_bookings():
    browser = mechanicalsoup.Browser(soup_config={"features": "html.parser"})

    try:
        login_page = browser.get('https://inbox.myallocator.com/en/login', timeout=15)
    except requests.exceptions.Timeout:
        print("timed out")
        return
    except requests.exceptions.ConnectionError:
        print("connections lost")
        return

    login_form = login_page.soup.select('.login_box')[0].select('form')[0]

    login_form.select('#Username')[0]['value'] = os.environ['MYALLOCATOR_USERNAME']
    login_form.select('#Password')[0]['value'] = os.environ['MYALLOCATOR_PASSWORD']

    browser.submit(login_form, login_page.url)

    csv_data = {
        'criteria': 'start_days',
        'timespan': '900',
        'filter': ''
    }

    try:
        response = browser.post(
            "https://inbox.myallocator.com/dispatch/csv_export/898/bookings.csv",
            csv_data, timeout=300)
    except requests.exceptions.Timeout:
        print("connection lost")
        return

    file_name = "bookings.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as bookings:
        bookings.write(response.content.decode('utf8'))

def add_to_database():
    logger = get_task_logger(__name__)
    with open('bookings.csv', encoding='utf-8') as file_read:
        bookings_csv = csv.reader(file_read)
        next(bookings_csv)
        for row in bookings_csv:
            if row[11] != '' and not Booking.objects.filter(booking_id=row[0]).exists():
                booking = Booking(
                    booking_id=row[0].strip(),
                    channel=row[1].strip(),
                    booking_date=datetime.strptime(row[2], '%Y-%m-%d'),
                    booking_time=datetime.strptime(row[5], '%H:%M:%S'),
                    arrival_date=datetime.strptime(row[6], '%Y-%m-%d'),
                    departure_date=datetime.strptime(row[7], '%Y-%m-%d'),
                    nights=int(row[8]),
                    first_name=row[11].strip(),
                    last_name=row[10].strip(),
                    email=row[12].strip(),
                    pax=int(row[16]),
                    room_names=row[18].split(', ')[0],
                    total_price=float(row[19]),
                    deposit=float(row[21])
                )
                booking.save()
                logger.info('Added booking {} for {} {} to database'.format(row[0], row[11], row[10]))
