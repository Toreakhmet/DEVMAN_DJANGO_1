
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from places.views import home_view, get_place

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view),
    path('place/<int:place_id>/', get_place, name='place_details'),
    path('tinymce/', include('tinymce.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
