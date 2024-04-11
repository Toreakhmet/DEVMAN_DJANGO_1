from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place

JSON_DUMPS_PARAMS = {
    'indent': 2,
    'ensure_ascii': False
}


def home_view(request):
    places = Place.objects.select_related('images').all()
    features = []
    for place in places:
        images = place.images.all().order_by('position')
        images_urls = [image.img.url for image in images]
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.latitude, place.longitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('place_details', kwargs={'place_id': place.id}),
                "images": images_urls
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


def get_place(request, place_id):
    place = get_object_or_404(
        Place.objects.select_related('images'), id=place_id)

    images_urls = [
        image.img.url for image in place.images.all().order_by('position')]

    context = {
        "title": place.title,
        "images": images_urls,
        "short_description": place.short_description,
        "long_description": place.long_description,
        "coordinates": {
            "lat": place.latitude,
            "lng": place.longitude
            
        }
    }

    return JsonResponse(
        context,
        json_dumps_params=JSON_DUMPS_PARAMS
    )
