from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0015_alter_photoarticle_apres_paragraphe"),
    ]

    operations = [
        migrations.AddField(
            model_name="demandepublicite",
            name="photo",
            field=models.FileField(
                blank=True,
                upload_to="demandes_publicites/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "webp", "avif", "gif"],
                        message="Ajoutez une image valide: JPG, PNG, WEBP, AVIF ou GIF.",
                    )
                ],
            ),
        ),
    ]
