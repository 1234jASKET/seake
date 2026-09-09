from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, Categorie


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = "https"

    def items(self):
        return Article.objects.filter(publie=True)

    def lastmod(self, obj):
        return obj.date_modification


class CategorieSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return Categorie.objects.all()


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def items(self):
        return [
            "accueil",
            "aujourd_hui",
            "sondage_election",
            "articles",
            "publicite",
            "abonnement",
            "contact",
            "a_propos",
        ]

    def location(self, item):
        return reverse(item)
