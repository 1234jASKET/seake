from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentaireForm, DemandePubliciteForm
from .models import Article, Categorie, EchantillonCouleur


def _articles_publies():
    return Article.objects.filter(publie=True).select_related("categorie")


def _article_layout(article_obj):
    paragraphs = [
        line.strip()
        for line in article_obj.contenu.splitlines()
        if line.strip()
    ]
    photos = list(article_obj.photos.all())
    photos_by_paragraph = {}
    gallery_photos = []

    for photo in photos:
        if photo.apres_paragraphe:
            position = min(photo.apres_paragraphe, max(len(paragraphs), 1))
            photos_by_paragraph.setdefault(position, []).append(photo)
        else:
            gallery_photos.append(photo)

    ad_position = article_obj.publicite_apres_paragraphe
    if ad_position and paragraphs:
        ad_position = min(ad_position, len(paragraphs))

    blocks = []
    for position, paragraph in enumerate(paragraphs, start=1):
        blocks.append({"type": "paragraph", "text": paragraph})
        for photo in photos_by_paragraph.get(position, []):
            blocks.append({"type": "photo", "photo": photo})
        if ad_position == position:
            blocks.append({"type": "advertisement"})

    return blocks, gallery_photos, bool(ad_position)


def accueil(request):
    articles = _articles_publies()[:3]
    categories = Categorie.objects.all()[:4]
    return render(
        request,
        "accueil.html",
        {"articles": articles, "categories": categories},
    )


def articles(request):
    return render(request, "articles.html", {"articles": _articles_publies()})


def ecran_actualites(request):
    articles = _articles_publies().prefetch_related("photos")[:12]
    publicites = [
        {
            "titre": "Votre entreprise ici",
            "texte": "Contactez SEAKE JOURNAL pour annoncer vos services sur nos ecrans.",
            "lien": "https://site.seakejournal.com/publicite/demande/",
        },
        {
            "titre": "Abonnez-vous a SEAKE JOURNAL",
            "texte": "Recevez des articles clairs sur l'actualite locale, nationale et internationale.",
            "lien": "https://www.seakejournal.com/",
        },
    ]
    return render(
        request,
        "ecran_actualites.html",
        {
            "articles": articles,
            "publicites": publicites,
        },
    )


def article(request, slug):
    article_obj = get_object_or_404(
        _articles_publies().prefetch_related("photos"),
        slug=slug,
    )
    if request.method == "POST":
        commentaire_form = CommentaireForm(request.POST)
        if commentaire_form.is_valid():
            commentaire = commentaire_form.save(commit=False)
            commentaire.article = article_obj
            commentaire.save()
            messages.success(
                request,
                "Merci. Votre commentaire sera visible apres verification.",
            )
            return redirect(article_obj.get_absolute_url())
    else:
        commentaire_form = CommentaireForm()

    articles_lies = (
        _articles_publies()
        .filter(categorie=article_obj.categorie)
        .exclude(pk=article_obj.pk)[:3]
    )
    commentaires = article_obj.commentaires.filter(approuve=True)
    article_blocks, gallery_photos, advertisement_is_inline = _article_layout(
        article_obj
    )
    return render(
        request,
        "article.html",
        {
            "article": article_obj,
            "articles_lies": articles_lies,
            "commentaire_form": commentaire_form,
            "commentaires": commentaires,
            "article_url": request.build_absolute_uri(article_obj.get_absolute_url()),
            "article_blocks": article_blocks,
            "gallery_photos": gallery_photos,
            "advertisement_is_inline": advertisement_is_inline,
        },
    )


def categories(request):
    categories_list = Categorie.objects.prefetch_related("articles")
    return render(request, "categories.html", {"categories": categories_list})


def categorie(request, slug):
    categorie_obj = get_object_or_404(Categorie, slug=slug)
    articles_categorie = _articles_publies().filter(categorie=categorie_obj)
    return render(
        request,
        "categorie.html",
        {"categorie": categorie_obj, "articles": articles_categorie},
    )


def contact(request):
    return render(request, "contact.html")


def a_propos(request):
    return render(request, "a_propos.html")


def impression(request):
    articles = _articles_publies()[:3]
    return render(request, "impression.html", {"articles": articles})


def publicite(request):
    return render(request, "publicite.html")


def demande_publicite(request):
    if request.method == "POST":
        form = DemandePubliciteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Votre demande a ete envoyee. SEAKE JOURNAL vous contactera bientot.",
            )
            return redirect("demande_publicite")
    else:
        form = DemandePubliciteForm()

    return render(request, "demande_publicite.html", {"form": form})


def coupons(request):
    return render(request, "coupons.html")


def reseaux_sociaux(request):
    articles = _articles_publies()[:6]
    return render(request, "reseaux_sociaux.html", {"articles": articles})


def color_control(request):
    echantillons = EchantillonCouleur.objects.all()[:12]
    return render(
        request,
        "color_control.html",
        {"echantillons": echantillons},
    )


def color_control_studio(request):
    return render(request, "color_control_studio.html")


def color_control_phone_scan(request):
    return render(request, "color_control_phone_scan.html")


def color_control_sample_timer(request):
    return render(request, "color_control_sample_timer.html")

# Create your views here.
