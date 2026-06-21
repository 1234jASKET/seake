from django.urls import path

from . import views
from .feeds import ArticlesFeed

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("articles/", views.articles, name="articles"),
    path("ecran/", views.ecran_actualites, name="ecran_actualites"),
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
    path("color-control/", views.color_control, name="color_control"),
    path("color-control/studio/", views.color_control_studio, name="color_control_studio"),
    path("color-control/phone-scan/", views.color_control_phone_scan, name="color_control_phone_scan"),
    path("color-control/sample-timer/", views.color_control_sample_timer, name="color_control_sample_timer"),
    path("flux/rss/", ArticlesFeed(), name="articles_feed"),
]
