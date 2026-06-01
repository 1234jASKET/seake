from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentaireForm, DemandePubliciteForm
from .models import Article, Categorie


def _articles_publies():
    return Article.objects.filter(publie=True).select_related("categorie")


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


def article(request, slug):
    article_obj = get_object_or_404(_articles_publies(), slug=slug)
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
    return render(
        request,
        "article.html",
        {
            "article": article_obj,
            "articles_lies": articles_lies,
            "commentaire_form": commentaire_form,
            "commentaires": commentaires,
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
    return render(request, "reseaux_sociaux.html")

# Create your views here.
