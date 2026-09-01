from django import forms

from .models import Abonne, Commentaire, DemandePublicite


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
