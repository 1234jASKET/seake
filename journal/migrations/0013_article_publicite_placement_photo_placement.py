from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0012_correctionformule"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="publicite_apres_paragraphe",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text=(
                    "Numero du paragraphe apres lequel afficher la publicite. "
                    "Laissez vide pour l'afficher apres tout le texte."
                ),
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="photoarticle",
            name="apres_paragraphe",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text=(
                    "Exemple: 3 affiche la photo apres le 3e paragraphe. "
                    "Laissez vide pour la galerie a la fin."
                ),
                null=True,
            ),
        ),
    ]
