from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Article  # Предполагая, что у вас есть эти модели

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'home',
            'register',
            'login',
            'profile',
            'edit_profile',
            'services',
            'about',
            'order',
            'contacts',
            'articles',
            'reviews',
            'callback_request',
        ]

    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Предполагая, что у модели есть это поле

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at