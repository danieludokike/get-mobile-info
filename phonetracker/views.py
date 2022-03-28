from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

import geocoder
import folium
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from phonenumbers import geocoder as gc

from opencage.geocoder import OpenCageGeocode
API_KEY = '7476c3ecd37f46f7adc97545829376ad'


def home(request):
    """Renders the home page on request"""
    template = "index.html"
    return render(request, template)


def track_phone_view(request):
    """Accepts the phone number and track it"""
    template = "phone_info.html"
    if request.method == "POST":
        try:
            target_num = phonenumbers.parse(request.POST.get("phone_number"))
        except phonenumbers.NumberParseException as err:
            messages.info(request, f"{err}")
            return redirect("home")

        # CHECKING IF THE NUMBER IS VALID
        if not carrier._is_mobile(number_type(target_num)):
            messages.info(request, "Invalid phone number")
            return redirect("home")

        phone_number = request.POST.get("phone_number")
        location = gc.description_for_number(target_num, lang="en")
        phone_carrier = carrier.name_for_number(target_num, lang="en")

        geo_code = OpenCageGeocode(API_KEY)
        query = str(location)
        result = geo_code.geocode(query)
        lat = None
        lng = None
        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
        map_link = f"https://maps.google.com/?q={lat},{lng}"
        # phone_location = folium.Map(location=[lat, lng], zoom_start=12, width=1000, height=1000, control_scale=True)
        # folium.Marker([lat, lng], popup=location).add_to(phone_location)
        # phone_location.save(f"{phone_number}.html")

        context = {
            "phone_number": phone_number,
            "phone_carrier": phone_carrier,
            "phone_location": location,
            "title": f"INFO FOR {phone_number}",
            "map_link": map_link,
        }
        return render(request, template, context)
    return redirect("<h1 style='color: red;'>Only post request can be handled</h1>")


def input_view(request):
    return render(request, "input.html", {"values": [1, 2, 3, 4, 5, 6, 7]})