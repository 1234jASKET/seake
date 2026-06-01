from django import forms

from .models import Commentaire, DemandePublicite


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
