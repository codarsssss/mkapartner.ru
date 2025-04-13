from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from homeapp.admin import custom_admin_site

app_name = 'homeapp'

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('homeapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
