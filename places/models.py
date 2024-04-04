from django.db import models

# Create your models here.
class Place(models.Model):
    title = models.CharField("Заголовок", max_length=200, db_index=True)
    description_short = models.CharField("Описание короткое", max_length=512)
    description_long = models.TextField("Описание длинное")
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')

    def __str__(self):
        return f'{self.title}'