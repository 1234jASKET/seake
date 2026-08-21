from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0016_demandepublicite_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="demandepublicite",
            name="video",
            field=models.FileField(
                blank=True,
                upload_to="demandes_publicites/videos/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["mp4", "webm", "mov", "m4v"],
                        message="Ajoutez une video valide: MP4, WEBM, MOV ou M4V.",
                    )
                ],
            ),
        ),
    ]
