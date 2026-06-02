from django.urls import path

from . import views
from .feeds import ArticlesFeed

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("articles/", views.articles, name="articles"),
    path("articles/<slug:slug>/", views.article, name="article"),
    path("categories/", views.categories, name="categories"),
    path("categories/<slug:slug>/", views.categorie, name="categorie"),
    path("contact/", views.contact, name="contact"),
    path("a-propos/", views.a_propos, name="a_propos"),
    path("impression/", views.impression, name="impression"),
    path("publicite/", views.publicite, name="publicite"),
    path("publicite/demande/", views.demande_publicite, name="demande_publicite"),
    path("coupons/", views.coupons, name="coupons"),
    path("reseaux-sociaux/", views.reseaux_sociaux, name="reseaux_sociaux"),
    path("flux/rss/", ArticlesFeed(), name="articles_feed"),
]
