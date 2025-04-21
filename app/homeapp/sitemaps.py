from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News, Article, Service, PracticeInstance

class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return News.published.all()

    def lastmod(self, obj):
        return obj.create_datetime

class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Article.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_at

class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Service.objects.filter(is_active=True)

class PracticeSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return PracticeInstance.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'homeapp:index',
            'homeapp:team',
            'homeapp:tariffs',
            'homeapp:reviews',
            'homeapp:client_list',
            'homeapp:article_list',
            'homeapp:video_list',
            'homeapp:news_list',
            'homeapp:cases',
            'homeapp:rabotaem',
            'homeapp:polnomochiya',
            'homeapp:tayna',
            'homeapp:soglashenie',
            'homeapp:varianty',
            'homeapp:privicy',
        ]

    def location(self, item):
        return reverse(item)