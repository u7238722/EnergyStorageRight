from urllib.request import urlopen
import json
import reverse_geocode
# import geocoder
from geopy.geocoders import Nominatim
from geopy.point import Point

def get_country(lat,lon):
    geolocator = Nominatim(user_agent='demo_of_gnss_help')
    point=Point(lat,lon)
    try:
        location = geolocator.reverse(point)
        value = location.address.split(',')[-1]
        # area_code=location.address['country_code']
        return value,location.raw['address']['country_code'].upper()
    except TypeError:
        return ""

