from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import Article, Categorie, Commentaire, DemandePublicite, PhotoArticle


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "resume": forms.Textarea(
                attrs={
                    "rows": 4,
                    "style": "width: 100%; max-width: 980px;",
                }
            ),
            "contenu": forms.Textarea(
                attrs={
                    "rows": 24,
                    "style": "width: 100%; max-width: 980px; font-size: 16px; line-height: 1.6;",
                }
            ),
            "publicite_texte": forms.Textarea(
                attrs={
                    "rows": 8,
                    "style": "width: 100%; max-width: 980px;",
                }
            ),
        }


def render_image_preview(image_file):
    if not image_file:
        return "Aucune image"

    return format_html(
        '<img src="{}" style="height: 84px; width: 126px; object-fit: cover; border-radius: 6px;" />',
        image_file.url,
    )


class ImagePreviewAdminMixin:
    @admin.display(description="Apercu")
    def image_preview(self, obj):
        return render_image_preview(obj.image if obj else None)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "slug")
    prepopulated_fields = {"slug": ("nom",)}
    search_fields = ("nom", "description")


class PhotoArticleInline(ImagePreviewAdminMixin, admin.TabularInline):
    model = PhotoArticle
    extra = 4
    fields = ("image_preview", "image", "legende", "ordre")
    readonly_fields = ("image_preview",)


@admin.register(Article)
class ArticleAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = (
        "titre",
        "categorie",
        "auteur",
        "publie",
        "date_publication",
        "image_preview",
    )
    list_filter = ("publie", "categorie", "date_publication")
    prepopulated_fields = {"slug": ("titre",)}
    search_fields = ("titre", "resume", "contenu", "auteur")
    date_hierarchy = "date_publication"
    readonly_fields = ("image_preview", "publicite_image_preview")
    fieldsets = (
        (
            "Article",
            {
                "fields": (
                    "titre",
                    "slug",
                    "categorie",
                    "resume",
                    "contenu",
                    "auteur",
                )
            },
        ),
        (
            "Photo principale",
            {
                "fields": ("image_preview", "image"),
            },
        ),
        (
            "Publicite dans l'article",
            {
                "fields": (
                    "publicite_titre",
                    "publicite_texte",
                    "publicite_image_preview",
                    "publicite_image",
                    "publicite_lien",
                    "publicite_bouton",
                ),
                "description": (
                    "Utilisez cette section pour afficher une publicite au milieu de "
                    "l'article. Laissez vide si l'article n'a pas de publicite."
                ),
            },
        ),
        (
            "Publication",
            {
                "fields": ("publie", "date_publication"),
            },
        ),
    )
    inlines = [PhotoArticleInline]

    @admin.display(description="Apercu publicite")
    def publicite_image_preview(self, obj):
        return render_image_preview(obj.publicite_image if obj else None)


@admin.register(PhotoArticle)
class PhotoArticleAdmin(ImagePreviewAdminMixin, admin.ModelAdmin):
    list_display = ("image_preview", "article", "legende", "ordre")
    list_filter = ("article",)
    search_fields = ("article__titre", "legende")
    readonly_fields = ("image_preview",)


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
