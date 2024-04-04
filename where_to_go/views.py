from django.shortcuts import render
from django.urls import reverse
from places.models import Place

def HomeView(request):
    places = Place.objects.all()
    features = []
    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lon, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('place-place_details', kwargs={'place_id': place.id})
            }
        })
    places_geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    context = {
        "places_geojson": places_geojson,
    }
    return render(request, 'index.html', context)