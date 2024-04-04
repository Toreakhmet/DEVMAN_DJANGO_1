
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from places.views import get_place
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",HomeView),
    path('place/<int:place_id>/', get_place, name='place-place_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)