from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import (
    Article,
    Categorie,
    Commentaire,
    CorrectionFormule,
    DemandePublicite,
    EchantillonCouleur,
    LectureCouleur,
    PhotoArticle,
)


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
    fields = ("image_preview", "image", "legende", "apres_paragraphe")
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
                    "publicite_apres_paragraphe",
                ),
                "description": (
                    "Pour placer la publicite dans le texte, indiquez apres quel "
                    "paragraphe elle doit apparaitre. Laissez ce numero vide pour "
                    "l'afficher apres tout le texte."
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
    list_display = (
        "image_preview",
        "article",
        "legende",
        "apres_paragraphe",
        "ordre",
    )
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
        "photo_preview",
    )
    list_filter = ("type_produit", "statut", "date_creation")
    search_fields = ("nom_client", "nom_entreprise", "email", "telephone", "message")
    readonly_fields = ("date_creation", "photo_preview")
    fields = (
        "nom_client",
        "nom_entreprise",
        "email",
        "telephone",
        "type_produit",
        "budget",
        "date_souhaitee",
        "photo_preview",
        "photo",
        "message",
        "statut",
        "date_creation",
    )

    @admin.display(description="Photo")
    def photo_preview(self, obj):
        return render_image_preview(obj.photo if obj else None)


@admin.register(EchantillonCouleur)
class EchantillonCouleurAdmin(admin.ModelAdmin):
    list_display = (
        "nom_client",
        "projet",
        "couleur",
        "reference",
        "substrat",
        "blanc_soutien",
        "apercu_couleur",
        "moyenne_delta_e_display",
        "pire_delta_e_display",
        "resultat_display",
        "statut",
        "date_modification",
    )
    list_filter = ("statut", "substrat", "blanc_soutien", "date_creation", "date_modification")
    search_fields = ("nom_client", "projet", "couleur", "reference", "commentaire")
    readonly_fields = (
        "apercu_couleur",
        "delta_e_display",
        "moyenne_delta_e_display",
        "meilleur_delta_e_display",
        "pire_delta_e_display",
        "resultat_display",
        "date_creation",
        "date_modification",
    )
    inlines = []
    fieldsets = (
        (
            "Client et projet",
            {
                "fields": (
                    "nom_client",
                    "projet",
                    "couleur",
                    "reference",
                    "substrat",
                    "surface",
                    "blanc_soutien",
                    "couches_blanc",
                    "opacite_blanc",
                    "hex_couleur",
                    "apercu_couleur",
                )
            },
        ),
        (
            "Cible Lab",
            {
                "fields": ("cible_l", "cible_a", "cible_b"),
            },
        ),
        (
            "Mesure Lab principale",
            {
                "fields": ("mesure_l", "mesure_a", "mesure_b", "tolerance_delta_e"),
                "description": (
                    "Vous pouvez entrer une mesure principale ici. Pour plusieurs lectures, "
                    "utilisez aussi la section Lectures couleur plus bas."
                ),
            },
        ),
        (
            "Resultat",
            {
                "fields": (
                    "delta_e_display",
                    "moyenne_delta_e_display",
                    "meilleur_delta_e_display",
                    "pire_delta_e_display",
                    "resultat_display",
                    "statut",
                    "commentaire",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": ("date_creation", "date_modification"),
            },
        ),
    )

    @admin.display(description="Apercu")
    def apercu_couleur(self, obj):
        if not obj or not obj.apercu_hex:
            return "Apercu apres sauvegarde"
        return format_html(
            '<span style="display:inline-block;width:76px;height:32px;border:1px solid #ccc;border-radius:6px;background:{};"></span> <code>{}</code>',
            obj.apercu_hex,
            obj.apercu_hex,
        )

    @admin.display(description="Delta E")
    def delta_e_display(self, obj):
        delta_e = obj.delta_e
        if delta_e is None:
            return "En attente"
        return delta_e

    @admin.display(description="Moyenne Delta E")
    def moyenne_delta_e_display(self, obj):
        return obj.moyenne_delta_e if obj.moyenne_delta_e is not None else "En attente"

    @admin.display(description="Meilleur Delta E")
    def meilleur_delta_e_display(self, obj):
        return obj.meilleur_delta_e if obj.meilleur_delta_e is not None else "En attente"

    @admin.display(description="Pire Delta E")
    def pire_delta_e_display(self, obj):
        return obj.pire_delta_e if obj.pire_delta_e is not None else "En attente"

    @admin.display(description="Controle")
    def resultat_display(self, obj):
        resultat = obj.resultat
        color = "#20572a" if resultat == "Accepte" else "#9b1c1c"
        if resultat == "En attente de mesure":
            color = "#5d6b7a"
        return format_html('<strong style="color:{};">{}</strong>', color, resultat)


class LectureCouleurInline(admin.TabularInline):
    model = LectureCouleur
    extra = 5
    fields = (
        "ordre",
        "nom",
        "mesure_l",
        "mesure_a",
        "mesure_b",
        "delta_e_display",
        "resultat_display",
        "commentaire",
    )
    readonly_fields = ("delta_e_display", "resultat_display")

    @admin.display(description="Delta E")
    def delta_e_display(self, obj):
        if not obj or not obj.pk:
            return "Apres sauvegarde"
        return obj.delta_e

    @admin.display(description="Pass/Fail")
    def resultat_display(self, obj):
        if not obj or not obj.pk:
            return "Apres sauvegarde"
        color = "#20572a" if obj.resultat == "Pass" else "#9b1c1c"
        return format_html('<strong style="color:{};">{}</strong>', color, obj.resultat)


class CorrectionFormuleInline(admin.StackedInline):
    model = CorrectionFormule
    extra = 1
    fields = (
        "titre",
        "poids_batch",
        ("pro_blue_ajout", "green_ajout", "trans_white_reduction"),
        "autre_correction",
        ("mesure_apres_l", "mesure_apres_a", "mesure_apres_b"),
        "delta_e_apres_display",
        "resultat_apres_display",
        "commentaire",
        "date_creation",
    )
    readonly_fields = ("delta_e_apres_display", "resultat_apres_display", "date_creation")

    @admin.display(description="Delta E apres correction")
    def delta_e_apres_display(self, obj):
        if not obj or not obj.pk:
            return "Apres sauvegarde"
        return obj.delta_e_apres if obj.delta_e_apres is not None else "En attente"

    @admin.display(description="Pass/Fail apres correction")
    def resultat_apres_display(self, obj):
        if not obj or not obj.pk:
            return "Apres sauvegarde"
        color = "#20572a" if obj.resultat_apres == "Pass" else "#9b1c1c"
        if obj.resultat_apres == "En attente":
            color = "#5d6b7a"
        return format_html('<strong style="color:{};">{}</strong>', color, obj.resultat_apres)


EchantillonCouleurAdmin.inlines = [LectureCouleurInline, CorrectionFormuleInline]


@admin.register(LectureCouleur)
class LectureCouleurAdmin(admin.ModelAdmin):
    list_display = (
        "echantillon",
        "nom",
        "mesure_l",
        "mesure_a",
        "mesure_b",
        "delta_e_display",
        "resultat_display",
        "date_creation",
    )
    list_filter = ("echantillon__substrat", "date_creation")
    search_fields = ("echantillon__nom_client", "echantillon__couleur", "nom", "commentaire")
    readonly_fields = ("delta_e_display", "resultat_display", "date_creation")

    @admin.display(description="Delta E")
    def delta_e_display(self, obj):
        return obj.delta_e

    @admin.display(description="Pass/Fail")
    def resultat_display(self, obj):
        color = "#20572a" if obj.resultat == "Pass" else "#9b1c1c"
        return format_html('<strong style="color:{};">{}</strong>', color, obj.resultat)


@admin.register(CorrectionFormule)
class CorrectionFormuleAdmin(admin.ModelAdmin):
    list_display = (
        "echantillon",
        "titre",
        "poids_batch",
        "pro_blue_ajout",
        "green_ajout",
        "trans_white_reduction",
        "delta_e_apres_display",
        "resultat_apres_display",
        "date_creation",
    )
    list_filter = ("date_creation", "echantillon__substrat")
    search_fields = (
        "echantillon__nom_client",
        "echantillon__projet",
        "echantillon__couleur",
        "titre",
        "commentaire",
    )
    readonly_fields = ("delta_e_apres_display", "resultat_apres_display", "date_creation")

    @admin.display(description="Delta E apres")
    def delta_e_apres_display(self, obj):
        return obj.delta_e_apres if obj.delta_e_apres is not None else "En attente"

    @admin.display(description="Pass/Fail apres")
    def resultat_apres_display(self, obj):
        color = "#20572a" if obj.resultat_apres == "Pass" else "#9b1c1c"
        if obj.resultat_apres == "En attente":
            color = "#5d6b7a"
        return format_html('<strong style="color:{};">{}</strong>', color, obj.resultat_apres)


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("nom", "article", "approuve", "date_creation", "date_reponse")
    list_filter = ("approuve", "date_creation", "date_reponse")
    search_fields = ("nom", "email", "message", "reponse", "article__titre")
    readonly_fields = ("date_creation",)
    list_editable = ("approuve",)
