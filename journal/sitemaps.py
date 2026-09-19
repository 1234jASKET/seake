from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, Categorie, NumeroMagazine


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


class MagazineSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return NumeroMagazine.objects.filter(publie=True)

    def lastmod(self, obj):
        return obj.date_modification


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def items(self):
        return [
            "accueil",
            "aujourd_hui",
            "question_du_jour",
            "articles",
            "magazines",
            "publicite",
            "abonnement",
            "contact",
            "a_propos",
        ]

    def location(self, item):
        return reverse(item)
