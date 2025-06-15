from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from homeapp.admin import custom_admin_site
from homeapp.sitemaps import (
    NewsSitemap, ArticleSitemap, ServiceSitemap,
    PracticeSitemap, StaticViewSitemap,
)

app_name = 'homeapp'

# --- Карта сайта ---
sitemaps = {
    'static': StaticViewSitemap(),
    'news': NewsSitemap(),
    'articles': ArticleSitemap(),
    'services': ServiceSitemap(),
    'practices': PracticeSitemap(),
}

urlpatterns = [
    path("admin-backoffice/", custom_admin_site.urls),
    path("", include("homeapp.urls")),

    # Sitemap
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # Robots.txt
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
