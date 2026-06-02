from django.db import migrations
from django.utils import timezone


def creer_article_du_jour(apps, schema_editor):
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
        slug="elus-quebecois-condamnent-rassemblement-supremaciste-shawinigan",
        defaults={
            "titre": "Des elus quebecois condamnent un rassemblement supremaciste blanc a Shawinigan",
            "categorie": categorie,
            "resume": (
                "Un rassemblement supremaciste blanc tenu a Shawinigan a suscite de vives "
                "condamnations de la part de plusieurs responsables politiques quebecois."
            ),
            "contenu": (
                "Un rassemblement supremaciste blanc tenu samedi a Shawinigan, en Mauricie, "
                "a provoque de fortes reactions dans le monde politique quebecois.\n\n"
                "La manifestation s'est deroulee au parc des Veterans, pres du cenotaphe de "
                "la Ville de Shawinigan. Des individus masques y auraient brandi une banniere "
                "decoree de deux fleurs de lys et portant le message: "
                "\"Je me souviens d'un Quebec blanc\".\n\n"
                "Dans une declaration publiee dimanche, la premiere ministre du Quebec, "
                "Christine Frechette, a fermement condamne le rassemblement et les messages "
                "racistes qui y ont ete diffuses.\n\n"
                "Elle a affirme que de tels propos sont inacceptables et n'ont pas leur place "
                "dans la societe quebecoise. Selon elle, ce type de comportement ne represente "
                "ni le Quebec d'aujourd'hui ni celui que les Quebecois souhaitent batir. Elle "
                "a aussi insiste sur l'importance de ne jamais banaliser la haine ou le racisme.\n\n"
                "Le chef du Parti Quebecois, Paul St-Pierre Plamondon, a egalement reagi sur "
                "la plateforme X. Il a soutenu que certains groupes extremistes se cachent "
                "derriere des activites sportives pour recruter et normaliser leurs idees. "
                "Il a aussi rappele que les autorites de securite publique les identifient "
                "comme des groupes haineux.\n\n"
                "De son cote, le chef du Parti liberal du Quebec, Charles Milliard, a condamne "
                "sans reserve le rassemblement. Il a declare que ce message de division ne "
                "represente pas l'ouverture du peuple quebecois.\n\n"
                "Cet evenement relance les discussions sur la presence de groupes haineux au "
                "Quebec et sur l'importance de denoncer clairement les discours racistes "
                "lorsqu'ils apparaissent dans l'espace public."
            ),
            "auteur": "Equipe SEAKE JOURNAL",
            "publie": True,
            "date_publication": timezone.now(),
        },
    )


def retirer_article_du_jour(apps, schema_editor):
    Article = apps.get_model("journal", "Article")
    Article.objects.filter(
        slug="elus-quebecois-condamnent-rassemblement-supremaciste-shawinigan"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0004_commentaire"),
    ]

    operations = [
        migrations.RunPython(creer_article_du_jour, retirer_article_du_jour),
    ]
