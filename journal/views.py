from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AbonneForm,
    CommentaireForm,
    DemandePubliciteForm,
    ReponseSondageElectionForm,
)
from .models import Article, Categorie, DemandePublicite, EchantillonCouleur, InfoDuJour


def _articles_publies():
    return Article.objects.filter(publie=True).select_related("categorie")


def _article_layout(article_obj):
    photos = list(article_obj.photos.all())
    photos_by_marker = {}
    gallery_photos = []
    for photo in photos:
        if photo.apres_paragraphe:
            photos_by_marker.setdefault(photo.apres_paragraphe, []).append(photo)
        else:
            gallery_photos.append(photo)

    placement_markers = set(photos_by_marker) | {article_obj.publicite_apres_paragraphe}
    placement_markers.discard(None)
    explicit_markers = {
        int(line.strip())
        for line in article_obj.contenu.splitlines()
        if line.strip().isdigit() and int(line.strip()) in placement_markers
    }

    blocks = []
    paragraph_position = 0
    placed_photo_ids = set()
    advertisement_is_inline = False

    def place_marker(marker):
        nonlocal advertisement_is_inline
        for photo in photos_by_marker.get(marker, []):
            if photo.id in placed_photo_ids:
                continue
            blocks.append({"type": "photo", "photo": photo})
            placed_photo_ids.add(photo.id)
        if article_obj.publicite_apres_paragraphe == marker:
            blocks.append({"type": "advertisement"})
            advertisement_is_inline = True

    for line in article_obj.contenu.splitlines():
        paragraph = line.strip()
        if not paragraph:
            continue

        if paragraph.isdigit() and int(paragraph) in placement_markers:
            place_marker(int(paragraph))
            continue

        paragraph_position += 1
        blocks.append({"type": "paragraph", "text": paragraph})
        if paragraph_position not in explicit_markers:
            place_marker(paragraph_position)

    for marker in sorted(photos_by_marker):
        for photo in photos_by_marker[marker]:
            if photo.id not in placed_photo_ids:
                blocks.append({"type": "photo", "photo": photo})
                placed_photo_ids.add(photo.id)

    if (
        article_obj.publicite_apres_paragraphe
        and not advertisement_is_inline
    ):
        blocks.append({"type": "advertisement"})
        advertisement_is_inline = True

    return blocks, gallery_photos, advertisement_is_inline


def accueil(request):
    articles = _articles_publies()[:3]
    categories = Categorie.objects.all()[:4]
    return render(
        request,
        "accueil.html",
        {"articles": articles, "categories": categories},
    )


def aujourd_hui(request):
    info_du_jour = InfoDuJour.objects.filter(publie=True).first()
    articles_recents = _articles_publies().prefetch_related("photos")[:6]
    article_principal = articles_recents[0] if articles_recents else None
    articles_secondaires = articles_recents[1:6] if articles_recents else []
    publicites = DemandePublicite.objects.filter(
        statut=DemandePublicite.STATUT_ACCEPTEE,
    )[:3]
    date_du_jour = timezone.localdate()
    capsules = [
        {
            "titre": "Nouvelles du jour",
            "texte": "Les articles les plus recents publies par SEAKE JOURNAL.",
            "lien": "articles",
            "bouton": "Lire les nouvelles",
        },
        {
            "titre": "Coupons et aubaines",
            "texte": "Offres locales, annonces, rabais et commerces a decouvrir.",
            "lien": "coupons",
            "bouton": "Voir les coupons",
        },
        {
            "titre": "Publicites locales",
            "texte": "Maisons, logements, services, restaurants, outils et annonces client.",
            "lien": "publicite",
            "bouton": "Voir les annonces",
        },
        {
            "titre": "Cours couleur",
            "texte": "Livre couleur SEAKE, nuancier, encres, foil, papier et prépresse.",
            "lien": "color_control",
            "bouton": "Apprendre",
        },
    ]
    return render(
        request,
        "aujourd_hui.html",
        {
            "article_principal": article_principal,
            "articles_secondaires": articles_secondaires,
            "info_du_jour": info_du_jour,
            "publicites": publicites,
            "date_du_jour": date_du_jour,
            "capsules": capsules,
        },
    )


def articles(request):
    return render(request, "articles.html", {"articles": _articles_publies()})


def abonnement(request):
    if request.method == "POST":
        form = AbonneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Merci. Votre abonnement a ete ajoute a SEAKE JOURNAL.",
            )
            return redirect("abonnement")
    else:
        form = AbonneForm()

    articles_recents = _articles_publies()[:3]
    return render(
        request,
        "abonnement.html",
        {
            "form": form,
            "articles_recents": articles_recents,
        },
    )


def sondage_election(request):
    if request.method == "POST":
        form = ReponseSondageElectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Merci. Votre reponse au sondage SEAKE JOURNAL a ete recue.",
            )
            return redirect("sondage_election")
    else:
        form = ReponseSondageElectionForm()

    articles_recents = _articles_publies()[:3]
    return render(
        request,
        "sondage_election.html",
        {
            "form": form,
            "articles_recents": articles_recents,
        },
    )


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
    articles = _articles_publies()[:10]
    page1_publicite = DemandePublicite.objects.filter(
        type_produit=DemandePublicite.TYPE_PREMIERE_PAGE,
        statut=DemandePublicite.STATUT_ACCEPTEE,
    ).first()
    return render(
        request,
        "impression.html",
        {
            "articles": articles,
            "page1_publicite": page1_publicite,
        },
    )


def publicite(request):
    publicites_approuvees = DemandePublicite.objects.filter(
        statut=DemandePublicite.STATUT_ACCEPTEE,
    )[:12]
    return render(
        request,
        "publicite.html",
        {"publicites_approuvees": publicites_approuvees},
    )


def demande_publicite(request):
    if request.method == "POST":
        form = DemandePubliciteForm(request.POST, request.FILES)
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
