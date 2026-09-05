from django import forms

from .models import Abonne, Commentaire, DemandePublicite, ReponseSondageElection


class DemandePubliciteForm(forms.ModelForm):
    class Meta:
        model = DemandePublicite
        fields = [
            "nom_client",
            "nom_entreprise",
            "email",
            "telephone",
            "type_produit",
            "budget",
            "date_souhaitee",
            "photo",
            "video",
            "message",
        ]
        widgets = {
            "date_souhaitee": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Expliquez votre besoin: texte de l'annonce, coupon, date de publication, reseaux sociaux, etc.",
                }
            ),
        }
        labels = {
            "nom_client": "Votre nom",
            "nom_entreprise": "Nom de l'entreprise",
            "email": "Email",
            "telephone": "Telephone",
            "type_produit": "Produit souhaite",
            "budget": "Budget approximatif",
            "date_souhaitee": "Date souhaitee",
            "photo": "Photo de la publicite",
            "video": "Video de la publicite",
            "message": "Message",
        }


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ["nom", "email", "message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Ecrivez votre commentaire ou votre question.",
                }
            ),
        }
        labels = {
            "nom": "Votre nom",
            "email": "Email facultatif",
            "message": "Commentaire ou question",
        }


class AbonneForm(forms.ModelForm):
    consentement = forms.BooleanField(
        required=True,
        label="J'accepte de recevoir les nouvelles et communications de SEAKE JOURNAL.",
    )

    class Meta:
        model = Abonne
        fields = [
            "nom",
            "email",
            "telephone",
            "ville",
            "souhaite_courriel",
            "souhaite_sms",
        ]
        labels = {
            "nom": "Votre nom",
            "email": "Email",
            "telephone": "Telephone",
            "ville": "Ville ou quartier",
            "souhaite_courriel": "Recevoir par courriel",
            "souhaite_sms": "Recevoir par texto",
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        telephone = cleaned_data.get("telephone")
        if not email and not telephone:
            raise forms.ValidationError(
                "Ajoutez au moins un email ou un numero de telephone."
            )
        return cleaned_data


class ReponseSondageElectionForm(forms.ModelForm):
    consentement = forms.BooleanField(
        required=True,
        label=(
            "J'accepte que ma reponse anonyme soit utilisee pour un resume "
            "journalistique de SEAKE JOURNAL."
        ),
    )

    class Meta:
        model = ReponseSondageElection
        fields = [
            "region",
            "enjeu_important",
            "intention_vote",
            "certitude",
            "commentaire",
            "veut_resultats",
            "email",
        ]
        widgets = {
            "commentaire": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Votre commentaire facultatif.",
                }
            ),
            "intention_vote": forms.RadioSelect,
            "enjeu_important": forms.RadioSelect,
            "certitude": forms.RadioSelect,
        }
        labels = {
            "region": "Ville ou region",
            "enjeu_important": "Quel enjeu est le plus important pour vous?",
            "intention_vote": "Quel parti vous interesse le plus en ce moment?",
            "certitude": "Votre choix est-il certain?",
            "commentaire": "Commentaire facultatif",
            "veut_resultats": "Je veux recevoir les resultats",
            "email": "Email facultatif pour recevoir les resultats",
        }

    def clean(self):
        cleaned_data = super().clean()
        veut_resultats = cleaned_data.get("veut_resultats")
        email = cleaned_data.get("email")
        if veut_resultats and not email:
            raise forms.ValidationError(
                "Ajoutez votre email si vous voulez recevoir les resultats."
            )
        return cleaned_data
