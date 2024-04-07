from django.db import models


class Place(models.Model):
    title = models.CharField(
        max_length=200, db_index=True, verbose_name="Название")
    short_description = models.TextField("Короткое описание", blank=True)
    long_description = models.TextField("Длинное описание", blank=True)
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    image = models.ImageField("Изображение", upload_to='images/')
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name='Место', related_name='images')
    position = models.IntegerField(
        verbose_name='Позиция', db_index=True, default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.position}:{self.place}"
