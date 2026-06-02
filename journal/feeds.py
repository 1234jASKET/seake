from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Article


class ArticlesFeed(Feed):
    title = "SEAKE JOURNAL"
    link = "/articles/"
    description = "Les derniers articles publies sur SEAKE JOURNAL."

    def items(self):
        return Article.objects.filter(publie=True).select_related("categorie")[:20]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.resume

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.date_publication

    def item_categories(self, item):
        return [item.categorie.nom]

    def link(self):
        return reverse("articles")
