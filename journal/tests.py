import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .feeds import article_html
from .models import Article, Categorie, PhotoArticle


GIF_IMAGE = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
    b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ArticleMediaPlacementTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        categorie, _ = Categorie.objects.get_or_create(
            slug="actualites",
            defaults={"nom": "Actualites"},
        )
        self.article = Article.objects.create(
            titre="Article avec photos",
            slug="article-avec-photos",
            categorie=categorie,
            resume="Un resume.",
            contenu="Premier paragraphe.\n\nDeuxieme paragraphe.\n\nTroisieme paragraphe.",
            publicite_titre="SEAKE JOURNAL",
            publicite_texte="Abonnez-vous.",
            publicite_apres_paragraphe=2,
            publie=True,
            date_publication=timezone.now(),
        )
        self.photo = PhotoArticle.objects.create(
            article=self.article,
            image=SimpleUploadedFile("photo.gif", GIF_IMAGE, content_type="image/gif"),
            legende="Photo entre les paragraphes",
            apres_paragraphe=1,
        )

    def test_public_article_places_photo_and_ad_between_paragraphs(self):
        response = self.client.get(
            reverse("article", kwargs={"slug": self.article.slug})
        )

        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertLess(html.index("Premier paragraphe."), html.index(self.photo.image.url))
        self.assertLess(html.index(self.photo.image.url), html.index("Deuxieme paragraphe."))
        self.assertLess(html.index("Deuxieme paragraphe."), html.index("Abonnez-vous."))
        self.assertLess(html.index("Abonnez-vous."), html.index("Troisieme paragraphe."))

    def test_rss_places_photo_and_ad_between_paragraphs(self):
        html = article_html(self.article)

        self.assertLess(html.index("Premier paragraphe."), html.index(self.photo.image.url))
        self.assertLess(html.index(self.photo.image.url), html.index("Deuxieme paragraphe."))
        self.assertLess(html.index("Deuxieme paragraphe."), html.index("Abonnez-vous."))
        self.assertLess(html.index("Abonnez-vous."), html.index("Troisieme paragraphe."))
