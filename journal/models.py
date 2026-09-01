from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import math


image_file_validator = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png", "webp", "avif", "gif"],
    message="Ajoutez une image valide: JPG, PNG, WEBP, AVIF ou GIF.",
)


video_file_validator = FileExtensionValidator(
    allowed_extensions=["mp4", "webm", "mov", "m4v"],
    message="Ajoutez une video valide: MP4, WEBM, MOV ou M4V.",
)


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
    image = models.FileField(
        upload_to="articles/",
        blank=True,
        validators=[image_file_validator],
    )
    publicite_titre = models.CharField(max_length=160, blank=True)
    publicite_texte = models.TextField(blank=True)
    publicite_image = models.FileField(
        upload_to="articles/publicites/",
        blank=True,
        validators=[image_file_validator],
    )
    publicite_lien = models.URLField(blank=True)
    publicite_bouton = models.CharField(max_length=80, blank=True)
    publicite_apres_paragraphe = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text=(
            "Numero du paragraphe apres lequel afficher la publicite. "
            "Laissez vide pour l'afficher apres tout le texte."
        ),
    )
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
    image = models.FileField(
        upload_to="articles/galerie/",
        validators=[image_file_validator],
    )
    legende = models.CharField(max_length=180, blank=True)
    ordre = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre dans la galerie",
    )
    apres_paragraphe = models.PositiveSmallIntegerField(
        verbose_name="Afficher apres le paragraphe",
        blank=True,
        null=True,
        help_text=(
            "Exemple: 3 affiche la photo apres le 3e paragraphe. "
            "Pour un placement exact, ajoutez une ligne seule avec ce numero "
            "dans le texte de l'article. Laissez vide pour la galerie a la fin."
        ),
    )

    class Meta:
        ordering = ["ordre", "id"]

    def __str__(self):
        return self.legende or f"Photo pour {self.article}"


class DemandePublicite(models.Model):
    TYPE_PAGE = "page"
    TYPE_PREMIERE_PAGE = "premiere_page"
    TYPE_CARTE = "carte"
    TYPE_COUPON = "coupon"
    TYPE_RESEAUX = "reseaux"
    TYPE_CHOICES = [
        (TYPE_PAGE, "Page publicitaire"),
        (TYPE_PREMIERE_PAGE, "Demi-page premiere page"),
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
    photo = models.FileField(
        upload_to="demandes_publicites/",
        blank=True,
        validators=[image_file_validator],
    )
    video = models.FileField(
        upload_to="demandes_publicites/videos/",
        blank=True,
        validators=[video_file_validator],
    )
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


class InfoDuJour(models.Model):
    titre = models.CharField(
        max_length=180,
        default="Aujourd'hui sur SEAKE",
    )
    sous_titre = models.TextField(
        blank=True,
        default=(
            "Les nouvelles, annonces, coupons, cours et services utiles au meme "
            "endroit pour garder la communaute branchee."
        ),
    )
    photo = models.FileField(
        upload_to="infos_du_jour/",
        blank=True,
        validators=[image_file_validator],
        help_text="Photo principale pour la page Aujourd'hui sur SEAKE.",
    )
    meteo = models.CharField(max_length=220, blank=True)
    trafic = models.CharField(max_length=220, blank=True)
    evenement = models.CharField(max_length=220, blank=True)
    alerte = models.CharField(max_length=220, blank=True)
    message = models.TextField(blank=True)
    publie = models.BooleanField(default=True)
    date_affichage = models.DateField(default=timezone.localdate)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_affichage", "-date_modification"]
        verbose_name = "Info du jour"
        verbose_name_plural = "Infos du jour"

    def __str__(self):
        return f"{self.date_affichage} - {self.titre}"


class Abonne(models.Model):
    SOURCE_SITE = "site"
    SOURCE_PAPIER = "papier"
    SOURCE_TELEPHONE = "telephone"
    SOURCE_CHOICES = [
        (SOURCE_SITE, "Site web"),
        (SOURCE_PAPIER, "Journal papier"),
        (SOURCE_TELEPHONE, "Telephone"),
    ]

    nom = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=40, blank=True)
    ville = models.CharField(max_length=120, blank=True)
    souhaite_courriel = models.BooleanField(default=True)
    souhaite_sms = models.BooleanField(default=False)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_SITE)
    actif = models.BooleanField(default=True)
    note = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Abonne"
        verbose_name_plural = "Abonnes"

    def __str__(self):
        contact = self.email or self.telephone or "sans contact"
        return f"{self.nom} - {contact}"


class EchantillonCouleur(models.Model):
    STATUT_PREPARATION = "preparation"
    STATUT_APPROUVER = "a_approuver"
    STATUT_APPROUVE = "approuve"
    STATUT_REFUSE = "refuse"
    STATUT_CHOICES = [
        (STATUT_PREPARATION, "En preparation"),
        (STATUT_APPROUVER, "A approuver"),
        (STATUT_APPROUVE, "Approuve"),
        (STATUT_REFUSE, "Refuse"),
    ]
    SUBSTRAT_CHOICES = [
        ("papier_couche", "Papier couche"),
        ("papier_non_couche", "Papier non couche"),
        ("carton", "Carton"),
        ("film", "Film"),
        ("foil", "Foil"),
        ("plastique", "Plastique"),
        ("autre", "Autre"),
    ]

    nom_client = models.CharField(max_length=160)
    projet = models.CharField(max_length=180)
    couleur = models.CharField(max_length=120)
    reference = models.CharField(
        max_length=120,
        blank=True,
        help_text="Exemple: Pantone 485 C, CMYK, HEX ou reference client.",
    )
    substrat = models.CharField(
        max_length=30,
        choices=SUBSTRAT_CHOICES,
        default="papier_couche",
    )
    surface = models.CharField(
        max_length=120,
        blank=True,
        help_text="Exemple: brillant, mat, metallise, transparent.",
    )
    blanc_soutien = models.BooleanField(default=False)
    couches_blanc = models.PositiveSmallIntegerField(default=0)
    opacite_blanc = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Pourcentage optionnel, exemple: 85.00.",
    )
    hex_couleur = models.CharField(
        max_length=7,
        blank=True,
        help_text="Exemple: #D81818 pour afficher un apercu.",
    )
    cible_l = models.DecimalField(max_digits=6, decimal_places=2)
    cible_a = models.DecimalField(max_digits=6, decimal_places=2)
    cible_b = models.DecimalField(max_digits=6, decimal_places=2)
    mesure_l = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mesure_a = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mesure_b = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tolerance_delta_e = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_PREPARATION,
    )
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_modification"]
        verbose_name = "Echantillon couleur"
        verbose_name_plural = "Echantillons couleur"

    def __str__(self):
        return f"{self.nom_client} - {self.couleur}"

    @property
    def delta_e(self):
        mesure = self.mesures.order_by("ordre", "id").first()
        if mesure:
            return mesure.delta_e
        return self._calculate_delta_e(self.mesure_l, self.mesure_a, self.mesure_b)

    @property
    def resultat(self):
        if not self.delta_e_values:
            return "En attente de mesure"
        if self.pire_delta_e <= float(self.tolerance_delta_e):
            return "Accepte"
        return "Refuse"

    @property
    def delta_e_values(self):
        values = [mesure.delta_e for mesure in self.mesures.all() if mesure.delta_e is not None]
        if values:
            return values
        delta_e = self._calculate_delta_e(self.mesure_l, self.mesure_a, self.mesure_b)
        return [delta_e] if delta_e is not None else []

    @property
    def moyenne_delta_e(self):
        values = self.delta_e_values
        if not values:
            return None
        return round(sum(values) / len(values), 2)

    @property
    def meilleur_delta_e(self):
        values = self.delta_e_values
        if not values:
            return None
        return round(min(values), 2)

    @property
    def pire_delta_e(self):
        values = self.delta_e_values
        if not values:
            return None
        return round(max(values), 2)

    @property
    def apercu_hex(self):
        if self.hex_couleur:
            return self.hex_couleur
        if self.cible_l is None or self.cible_a is None or self.cible_b is None:
            return None
        return self._lab_to_srgb_hex(self.cible_l, self.cible_a, self.cible_b)

    def _calculate_delta_e(self, mesure_l, mesure_a, mesure_b):
        if mesure_l is None or mesure_a is None or mesure_b is None:
            return None

        delta_l = float(self.cible_l) - float(mesure_l)
        delta_a = float(self.cible_a) - float(mesure_a)
        delta_b = float(self.cible_b) - float(mesure_b)
        return round(math.sqrt(delta_l**2 + delta_a**2 + delta_b**2), 2)

    def _lab_to_srgb_hex(self, lab_l, lab_a, lab_b):
        l_value = float(lab_l)
        a_value = float(lab_a)
        b_value = float(lab_b)

        y = (l_value + 16) / 116
        x = a_value / 500 + y
        z = y - b_value / 200

        def lab_to_xyz_channel(value):
            if value**3 > 0.008856:
                return value**3
            return (value - 16 / 116) / 7.787

        x = 95.047 * lab_to_xyz_channel(x)
        y = 100.000 * lab_to_xyz_channel(y)
        z = 108.883 * lab_to_xyz_channel(z)

        x /= 100
        y /= 100
        z /= 100

        red = x * 3.2406 + y * -1.5372 + z * -0.4986
        green = x * -0.9689 + y * 1.8758 + z * 0.0415
        blue = x * 0.0557 + y * -0.2040 + z * 1.0570

        def srgb_channel(value):
            if value > 0.0031308:
                value = 1.055 * (value ** (1 / 2.4)) - 0.055
            else:
                value *= 12.92
            value = max(0, min(1, value))
            return round(value * 255)

        return "#{:02X}{:02X}{:02X}".format(
            srgb_channel(red),
            srgb_channel(green),
            srgb_channel(blue),
        )


class LectureCouleur(models.Model):
    echantillon = models.ForeignKey(
        EchantillonCouleur,
        on_delete=models.CASCADE,
        related_name="mesures",
    )
    nom = models.CharField(max_length=80, blank=True)
    mesure_l = models.DecimalField(max_digits=6, decimal_places=2)
    mesure_a = models.DecimalField(max_digits=6, decimal_places=2)
    mesure_b = models.DecimalField(max_digits=6, decimal_places=2)
    ordre = models.PositiveIntegerField(default=0)
    commentaire = models.CharField(max_length=180, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ordre", "id"]
        verbose_name = "Lecture couleur"
        verbose_name_plural = "Lectures couleur"

    def __str__(self):
        return self.nom or f"Lecture {self.ordre}"

    @property
    def delta_e(self):
        return self.echantillon._calculate_delta_e(
            self.mesure_l,
            self.mesure_a,
            self.mesure_b,
        )

    @property
    def resultat(self):
        if self.delta_e <= float(self.echantillon.tolerance_delta_e):
            return "Pass"
        return "Fail"


class CorrectionFormule(models.Model):
    echantillon = models.ForeignKey(
        EchantillonCouleur,
        on_delete=models.CASCADE,
        related_name="corrections",
    )
    titre = models.CharField(max_length=120, default="Correction")
    poids_batch = models.DecimalField(max_digits=8, decimal_places=2, default=1000.00)
    pro_blue_ajout = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    green_ajout = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    trans_white_reduction = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    autre_correction = models.CharField(max_length=180, blank=True)
    mesure_apres_l = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mesure_apres_a = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    mesure_apres_b = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    commentaire = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "Correction formule"
        verbose_name_plural = "Corrections formule"

    def __str__(self):
        return f"{self.echantillon} - {self.titre}"

    @property
    def delta_e_apres(self):
        return self.echantillon._calculate_delta_e(
            self.mesure_apres_l,
            self.mesure_apres_a,
            self.mesure_apres_b,
        )

    @property
    def resultat_apres(self):
        delta_e = self.delta_e_apres
        if delta_e is None:
            return "En attente"
        if delta_e <= float(self.echantillon.tolerance_delta_e):
            return "Pass"
        return "Fail"


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
