import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .feeds import article_html
from .models import (
    Article,
    Categorie,
    InfoDuJour,
    NumeroMagazine,
    PhotoArticle,
    QuestionDuJour,
    ReponseQuestionDuJour,
)


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
            contenu=(
                "Premier paragraphe.\n"
                "1\n"
                "Deuxieme paragraphe.\n"
                "2\n"
                "Troisieme paragraphe."
            ),
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
        self.assertNotIn("<p>1</p>", html)
        self.assertNotIn("<p>2</p>", html)

    def test_rss_places_photo_and_ad_between_paragraphs(self):
        html = article_html(self.article)

        self.assertLess(html.index("Premier paragraphe."), html.index(self.photo.image.url))
        self.assertLess(html.index(self.photo.image.url), html.index("Deuxieme paragraphe."))
        self.assertLess(html.index("Deuxieme paragraphe."), html.index("Abonnez-vous."))
        self.assertLess(html.index("Abonnez-vous."), html.index("Troisieme paragraphe."))
        self.assertNotIn("<p>1</p>", html)
        self.assertNotIn("<p>2</p>", html)


class QuestionDuJourTests(TestCase):
    def setUp(self):
        self.question = QuestionDuJour.objects.create(
            question="Quel sujet voulez-vous lire?",
            choix_1="Actualite locale",
            choix_2="Economie",
            choix_3="Sport",
            active=True,
            date_affichage=timezone.localdate(),
        )

    def test_question_is_visible_on_public_pages(self):
        question_response = self.client.get(reverse("question_du_jour"))
        accueil_response = self.client.get(reverse("accueil"))
        aujourd_hui_response = self.client.get(reverse("aujourd_hui"))

        self.assertContains(question_response, self.question.question)
        self.assertContains(accueil_response, self.question.question)
        self.assertContains(aujourd_hui_response, "Question du jour")

    def test_answer_is_saved_only_once_per_session(self):
        url = reverse("question_du_jour")

        first_response = self.client.post(url, {"choix": "2"})
        second_response = self.client.post(url, {"choix": "1"})

        self.assertRedirects(first_response, url)
        self.assertRedirects(second_response, url)
        self.assertEqual(ReponseQuestionDuJour.objects.count(), 1)
        self.assertEqual(ReponseQuestionDuJour.objects.get().choix, 2)

    def test_old_survey_link_redirects_to_question_of_the_day(self):
        response = self.client.get(reverse("sondage_election"))

        self.assertRedirects(
            response,
            reverse("question_du_jour"),
            status_code=301,
        )


class AccueilQuotidienTests(TestCase):
    def setUp(self):
        categorie = Categorie.objects.create(
            nom="Actualites",
            slug="actualites-accueil",
        )
        self.article = Article.objects.create(
            titre="La nouvelle principale du jour",
            slug="nouvelle-principale-du-jour",
            categorie=categorie,
            resume="Le resume quotidien de SEAKE JOURNAL.",
            contenu="Le contenu de la nouvelle.",
            publie=True,
        )
        self.info = InfoDuJour.objects.create(
            titre="Aujourd'hui a Montreal",
            sous_titre="Le point quotidien pour les lecteurs.",
            meteo="Soleil et maximum de 22 degres.",
            trafic="Circulation dense sur les grands axes.",
            evenement="Un evenement a surveiller.",
            publie=True,
        )

    def test_accueil_uses_daily_information_and_latest_article(self):
        response = self.client.get(reverse("accueil"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SEAKE JOURNAL")
        self.assertContains(response, self.article.titre)
        self.assertContains(response, self.info.meteo)
        self.assertContains(response, self.info.trafic)
        self.assertContains(response, "La chaîne YouTube")

    def test_accueil_still_renders_without_daily_content(self):
        Article.objects.all().delete()
        InfoDuJour.objects.all().delete()

        response = self.client.get(reverse("accueil"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "La prochaine edition se prepare")


class MagazineTests(TestCase):
    def setUp(self):
        categorie = Categorie.objects.create(
            nom="Magazine",
            slug="magazine-test",
        )
        self.article = Article.objects.create(
            titre="Un grand dossier SEAKE",
            slug="grand-dossier-seake",
            categorie=categorie,
            resume="Un dossier retenu pour le magazine.",
            contenu="Contenu du dossier.",
            publie=True,
        )
        self.numero = NumeroMagazine.objects.create(
            titre="Le premier magazine SEAKE",
            slug="premier-magazine-seake",
            sous_titre="Une edition numerique et papier.",
            numero_edition="Volume 1, numero 1",
            editorial="Bienvenue dans ce premier numero.",
            nombre_pages=8,
            publie=True,
        )
        self.numero.articles.add(self.article)

    def test_magazine_list_shows_published_issue(self):
        response = self.client.get(reverse("magazines"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.numero.titre)
        self.assertContains(response, self.numero.numero_edition)

    def test_magazine_detail_shows_selected_articles(self):
        response = self.client.get(self.numero.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.numero.editorial)
        self.assertContains(response, self.article.titre)

    def test_unpublished_issue_is_not_public(self):
        self.numero.publie = False
        self.numero.save(update_fields=["publie"])

        response = self.client.get(self.numero.get_absolute_url())

        self.assertEqual(response.status_code, 404)
