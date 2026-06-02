from django.db import models
from django.urls import reverse
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("categorie", kwargs={"slug": self.slug})


class Article(models.Model):
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    resume = models.CharField(max_length=280)
    contenu = models.TextField()
    auteur = models.CharField(max_length=120, default="Equipe SEAKE JOURNAL")
    image = models.FileField(upload_to="articles/", blank=True)
    publie = models.BooleanField(default=True)
    date_publication = models.DateTimeField(default=timezone.now)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_publication"]

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})


class PhotoArticle(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.FileField(upload_to="articles/galerie/")
    legende = models.CharField(max_length=180, blank=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "id"]

    def __str__(self):
        return self.legende or f"Photo pour {self.article}"


class DemandePublicite(models.Model):
    TYPE_PAGE = "page"
    TYPE_CARTE = "carte"
    TYPE_COUPON = "coupon"
    TYPE_RESEAUX = "reseaux"
    TYPE_CHOICES = [
        (TYPE_PAGE, "Page publicitaire"),
        (TYPE_CARTE, "Carte d'affaire"),
        (TYPE_COUPON, "Coupon rabais"),
        (TYPE_RESEAUX, "Campagne reseaux sociaux"),
    ]

    STATUT_NOUVELLE = "nouvelle"
    STATUT_CONTACTE = "contacte"
    STATUT_ACCEPTEE = "acceptee"
    STATUT_REFUSEE = "refusee"
    STATUT_CHOICES = [
        (STATUT_NOUVELLE, "Nouvelle"),
        (STATUT_CONTACTE, "Client contacte"),
        (STATUT_ACCEPTEE, "Acceptee"),
        (STATUT_REFUSEE, "Refusee"),
    ]

    nom_client = models.CharField(max_length=160)
    nom_entreprise = models.CharField(max_length=180, blank=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=40, blank=True)
    type_produit = models.CharField(max_length=20, choices=TYPE_CHOICES)
    budget = models.CharField(max_length=80, blank=True)
    date_souhaitee = models.DateField(blank=True, null=True)
    message = models.TextField()
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_NOUVELLE,
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"{self.nom_client} - {self.get_type_produit_display()}"


class Commentaire(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="commentaires",
    )
    nom = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    message = models.TextField()
    reponse = models.TextField(blank=True)
    approuve = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Commentaire de {self.nom} sur {self.article}"

    def save(self, *args, **kwargs):
        if self.reponse and not self.date_reponse:
            self.date_reponse = timezone.now()
        super().save(*args, **kwargs)
