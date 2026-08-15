from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

import phonenumbers
from phonenumbers import geocoder, carrier

import folium
from opencage.geocoder import OpenCageGeocode

from config import settings
from map.forms import PhoneSearchForm
from map.models import PhoneSearch


class MapView(LoginRequiredMixin, View):
    def get(self, request):
        recent_phones = PhoneSearch.objects.all().order_by('-id')[:5]
        return render(request, 'map/map.html', {
            'form': PhoneSearchForm(),
            'phones': recent_phones
        })

    def post(self, request):
        form = PhoneSearchForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']

            if not str(number).startswith('+'):
                number = '+' + str(number)

            if not phonenumbers.is_possible_number_string(number, None):
                messages.error(request, "Invalid phone number format")
                return render(request, 'map/map.html', {'form': form})

            parsed_number = phonenumbers.parse(number)

            if not phonenumbers.is_valid_number(parsed_number):
                messages.error(request, "Invalid phone number")
                return render(request, 'map/map.html', {'form': form})

            # location & provider
            location = geocoder.description_for_number(parsed_number, "en")
            provider = carrier.name_for_number(parsed_number, "en")

            if not location:
                messages.error(request, "Location not found")
                return render(request, 'map/map.html', {'form': form})

            if not settings.OPENCAGE_API_KEY:
                messages.error(request, "Geocoding API key missing")
                return render(request, 'map/map.html', {'form': form})

            geocoder_api = OpenCageGeocode(settings.OPENCAGE_API_KEY)
            results = geocoder_api.geocode(location)

            if not results:
                messages.error(request, "Geocoding failed")
                return render(request, 'map/map.html', {'form': form})

            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            time_zone = results[0]['annotations']['timezone']['name']

            # get_or_create
            phone, created = PhoneSearch.objects.get_or_create(
                number=number,
                defaults={
                    'location': location,
                    'provider': provider,
                    'latitude': lat,
                    'longitude': lng
                }
            )

            if created:
                messages.success(request, "New data saved")
            else:
                messages.info(request, "Existing data found")

            # Folium map
            my_map = folium.Map(location=[phone.latitude, phone.longitude], zoom_start=9)
            folium.Marker(
                [phone.latitude, phone.longitude],
                popup=f"{phone.location} ({phone.provider})"
            ).add_to(my_map)

            recent_phones = PhoneSearch.objects.all().order_by('-id')[:5]

            return render(request, 'map/map.html', {
                'form': form,
                'map': my_map._repr_html_(),
                'location': phone.location,
                'provider': phone.provider,
                'time_zone': time_zone,
                'phones': recent_phones
            })

        messages.error(request, "Invalid input")
        recent_phones = PhoneSearch.objects.all().order_by('-id')[:5]
        return render(request, 'map/map.html', {'form': form, 'phones': recent_phones})
