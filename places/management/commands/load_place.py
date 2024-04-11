from pathlib import Path
from urllib.parse import unquote

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned

from places.models import Place, Image

class Command(BaseCommand):
    help = 'Loads data from specified URLs into the database'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['urls']:
            response = requests.get(url)
            response.raise_for_status()
            payload = response.json()

            try:
                place, created = Place.objects.get_or_create(
                    title=payload['title'],
                    defaults={
                        'short_description': payload.get('short_description', ''),
                        'long_description': payload.get('long_description', ''),
                        'latitude': payload['coordinates']['lat'],
                        'longitude': payload['coordinates']['lng']
                    }
                )
            except MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'Multiple places found for title "{payload["title"]}". Skipping...'))
                continue

            for index, img_url in enumerate(payload['imgs']):
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                image_name = unquote(Path(img_url).name) # Parse image name correctly
                new_image = Image.objects.create(
                    place=place,
                    position=index,
                    image=ContentFile(img_response.content, name=image_name)
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from url "{url}"'))
