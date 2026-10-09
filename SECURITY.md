# Securite de SEAKE JOURNAL

## Protections actives

- HTTPS force en production avec cookies de session et CSRF securises.
- HSTS active pendant 30 jours, sans inclure automatiquement les sous-domaines.
- Cle secrete obligatoire dans l'environnement de production.
- Limitation des tentatives de connexion a l'administration.
- Limitation des envois repetes vers les formulaires publics.
- Champ invisible contre les robots sur les formulaires sensibles.
- Verification de la taille, de l'extension et de la signature des images, videos et PDF.
- Sessions fermees avec le navigateur et limitees a 12 heures.
- Protection contre l'integration du site dans une page externe.

## Verification avant chaque publication

1. Installer les versions de `requirements.txt`.
2. Executer `python manage.py check --deploy` avec les variables de production.
3. Executer `python manage.py test`.
4. Verifier que `DEBUG=False` sur Render.
5. Ne jamais placer un mot de passe, une cle API ou un fichier `.env` dans GitHub.

## Administration

- Utiliser un mot de passe unique et long pour chaque compte administrateur.
- Desactiver immediatement les anciens comptes d'administration.
- Ne jamais transmettre le mot de passe par courriel, texto ou capture d'ecran.
- Consulter regulierement la date de derniere connexion des comptes administrateurs.

## Sauvegardes

- Conserver une sauvegarde reguliere de PostgreSQL et du disque de medias Render.
- Tester periodiquement qu'une sauvegarde peut etre restauree.
- Conserver au moins une copie hors du serveur public.

## En cas d'incident

1. Mettre le site en maintenance si des donnees sont modifiees sans autorisation.
2. Changer la cle `SECRET_KEY` et les mots de passe administrateurs.
3. Revoquer toute cle externe exposee.
4. Examiner les journaux Render et restaurer une sauvegarde saine.
5. Installer toutes les mises a jour de securite avant la remise en ligne.
