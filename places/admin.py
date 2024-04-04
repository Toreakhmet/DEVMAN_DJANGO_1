from django.contrib import admin
from django.contrib.admin import TabularInline
from .models import Place,Image
# Register your models here.


class ImageInline(admin.TabularInline):
    model=Image
    extra=1

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines=[ImageInline]
admin.site.register(Image)