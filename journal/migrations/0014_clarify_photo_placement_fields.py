from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0013_article_publicite_placement_photo_placement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photoarticle",
            name="apres_paragraphe",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text=(
                    "Exemple: 3 affiche la photo apres le 3e paragraphe. "
                    "Laissez vide pour la galerie a la fin."
                ),
                null=True,
                verbose_name="Afficher apres le paragraphe",
            ),
        ),
        migrations.AlterField(
            model_name="photoarticle",
            name="ordre",
            field=models.PositiveIntegerField(
                default=0,
                verbose_name="Ordre dans la galerie",
            ),
        ),
    ]
