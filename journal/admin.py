from django.contrib import admin

from .models import Article, Categorie, Commentaire, DemandePublicite


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "slug")
    prepopulated_fields = {"slug": ("nom",)}
    search_fields = ("nom", "description")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "auteur", "publie", "date_publication")
    list_filter = ("publie", "categorie", "date_publication")
    prepopulated_fields = {"slug": ("titre",)}
    search_fields = ("titre", "resume", "contenu", "auteur")
    date_hierarchy = "date_publication"


@admin.register(DemandePublicite)
class DemandePubliciteAdmin(admin.ModelAdmin):
    list_display = (
        "nom_client",
        "nom_entreprise",
        "type_produit",
        "budget",
        "statut",
        "date_creation",
    )
    list_filter = ("type_produit", "statut", "date_creation")
    search_fields = ("nom_client", "nom_entreprise", "email", "telephone", "message")
    readonly_fields = ("date_creation",)


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("nom", "article", "approuve", "date_creation", "date_reponse")
    list_filter = ("approuve", "date_creation", "date_reponse")
    search_fields = ("nom", "email", "message", "reponse", "article__titre")
    readonly_fields = ("date_creation",)
    list_editable = ("approuve",)
