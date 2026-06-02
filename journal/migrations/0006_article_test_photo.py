from django.db import migrations
from django.utils import timezone


def creer_article_test_photo(apps, schema_editor):
    Categorie = apps.get_model("journal", "Categorie")
    Article = apps.get_model("journal", "Article")

    categorie, _ = Categorie.objects.get_or_create(
        slug="actualites",
        defaults={
            "nom": "Actualites",
            "description": "Les nouvelles importantes et les annonces de SEAKE JOURNAL.",
        },
    )

    Article.objects.update_or_create(
        slug="test-du-site-premier-article-avec-photo",
        defaults={
            "titre": "Test du site: premier article avec contenu et photo",
            "categorie": categorie,
            "resume": (
                "SEAKE JOURNAL teste l'affichage complet d'un article avec une image, "
                "un texte lisible, les boutons de partage et le flux RSS."
            ),
            "contenu": (
                "SEAKE JOURNAL poursuit ses tests avant la publication reguliere des articles. "
                "Ce texte sert a verifier que les lecteurs voient correctement le titre, le resume, "
                "la photo, le contenu complet et les options de partage.\n\n"
                "L'objectif est simple: publier un article dans l'administration Django et le voir "
                "apparaitre automatiquement sur le site public. Les lecteurs peuvent ensuite ouvrir "
                "l'article, lire le texte, poser une question et partager le lien sur les reseaux sociaux.\n\n"
                "Ce test permet aussi de confirmer que le flux RSS fonctionne pour Substack et les outils "
                "d'automatisation comme Make, Zapier ou Buffer. Le contenu complet doit etre disponible "
                "pour faciliter la reprise de l'article ailleurs.\n\n"
                "La prochaine etape sera d'ajouter des photos propres a chaque article depuis l'admin. "
                "Quand aucune photo n'est ajoutee, SEAKE JOURNAL affiche une image par defaut afin que "
                "la page reste visuelle et professionnelle."
            ),
            "auteur": "Equipe SEAKE JOURNAL",
            "publie": True,
            "date_publication": timezone.now(),
        },
    )


def retirer_article_test_photo(apps, schema_editor):
    Article = apps.get_model("journal", "Article")
    Article.objects.filter(slug="test-du-site-premier-article-avec-photo").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0005_article_du_jour"),
    ]

    operations = [
        migrations.RunPython(creer_article_test_photo, retirer_article_test_photo),
    ]
