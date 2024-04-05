from pathlib import Path
from urllib.parse import unquote

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['urls']:
            response = requests.get(url)
            response.raise_for_status()
            payload = response.json()

            place, created = Place.objects.get_or_create(
                title=payload['title'],
                defaults={
                    'description_short': payload['description_short'],
                    'description_long': payload['description_long'],
                    'lat': payload['coordinates']['lat'],
                    'lon': payload['coordinates']['lng']
                }
            )

            for index, img_url in enumerate(payload['imgs']):
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                content_file = ContentFile(img_response.content)
                new_image = Image(place=place, position=index)
                new_image.img.save(parse_img_name(img_url), content_file, save=False)
                new_image.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded url "{url}"'))


def parse_img_name(url):
    return Path(unquote(url)).name