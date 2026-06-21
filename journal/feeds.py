import mimetypes
from html import escape

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Enclosure, Rss201rev2Feed

from .models import Article


def public_url(path):
    site_url = getattr(settings, "PUBLIC_SITE_URL", "https://site.seakejournal.com")
    return f"{site_url.rstrip('/')}/{path.lstrip('/')}"


def image_html(image_file, alt):
    if not image_file:
        return ""

    return (
        f'<p><img src="{public_url(image_file.url)}" '
        f'alt="{escape(alt)}" style="max-width:100%;height:auto;" /></p>'
    )


def paragraphs_html(text):
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    return "".join(f"<p>{escape(paragraph).replace(chr(10), '<br>')}</p>" for paragraph in paragraphs)


def advertisement_html(item):
    if item.publicite_titre or item.publicite_texte or item.publicite_image:
        ad_button = ""
        if item.publicite_lien:
            button_text = item.publicite_bouton or "En savoir plus"
            ad_button = (
                f'<p><a href="{escape(item.publicite_lien)}">'
                f"{escape(button_text)}</a></p>"
            )
        return "".join(
            [
                "<hr>",
                "<p><strong>Publicite</strong></p>",
                image_html(item.publicite_image, item.publicite_titre or "Publicite"),
                f"<h2>{escape(item.publicite_titre)}</h2>" if item.publicite_titre else "",
                paragraphs_html(item.publicite_texte),
                ad_button,
            ]
        )
    return ""


def article_html(item):
    paragraphs = [
        line.strip()
        for line in item.contenu.splitlines()
        if line.strip()
    ]
    photos_by_paragraph = {}
    gallery_photos = []
    for photo in item.photos.all():
        if photo.apres_paragraphe:
            position = min(photo.apres_paragraphe, max(len(paragraphs), 1))
            photos_by_paragraph.setdefault(position, []).append(photo)
        else:
            gallery_photos.append(photo)

    ad_position = item.publicite_apres_paragraphe
    if ad_position and paragraphs:
        ad_position = min(ad_position, len(paragraphs))

    content_html = []
    for position, paragraph in enumerate(paragraphs, start=1):
        content_html.append(
            f"<p>{escape(paragraph).replace(chr(10), '<br>')}</p>"
        )
        content_html.extend(
            image_html(photo.image, photo.legende or item.titre)
            for photo in photos_by_paragraph.get(position, [])
        )
        if ad_position == position:
            content_html.append(advertisement_html(item))

    if not ad_position:
        content_html.append(advertisement_html(item))

    content_html.extend(
        image_html(photo.image, photo.legende or item.titre)
        for photo in gallery_photos
    )

    return "".join(
        [
            image_html(item.image, item.titre),
            f"<p><strong>{escape(item.resume)}</strong></p>",
            *content_html,
        ]
    )


class FullContentRssFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super().rss_attributes()
        attrs["xmlns:content"] = "http://purl.org/rss/1.0/modules/content/"
        return attrs

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        if item.get("content_encoded"):
            handler.startElement("content:encoded", {})
            handler.characters(item["content_encoded"])
            handler.endElement("content:encoded")


class ArticlesFeed(Feed):
    feed_type = FullContentRssFeed
    title = "SEAKE JOURNAL"
    link = "/articles/"
    description = "Les derniers articles publies sur SEAKE JOURNAL."

    def items(self):
        return (
            Article.objects.filter(publie=True)
            .exclude(slug__startswith="test-du-site")
            .select_related("categorie")
            .prefetch_related("photos")[:20]
        )

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return article_html(item)

    def item_extra_kwargs(self, item):
        return {"content_encoded": article_html(item)}

    def item_enclosures(self, item):
        if not item.image:
            return []

        mime_type, _ = mimetypes.guess_type(item.image.name)
        return [
            Enclosure(
                public_url(item.image.url),
                str(item.image.size),
                mime_type or "image/jpeg",
            )
        ]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.date_publication

    def item_categories(self, item):
        return [item.categorie.nom]

    def link(self):
        return reverse("articles")
