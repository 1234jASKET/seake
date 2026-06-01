# Deployer SEAKE JOURNAL avec Render et Namecheap

## 1. GitHub

1. Cree un depot GitHub, par exemple `seake-journal`.
2. Envoie ce projet sur GitHub.
3. Sur Render, choisis ce depot pour creer le service.

## 2. Render

Option recommandee:

1. Va dans Render > Blueprints > New Blueprint Instance.
2. Connecte ton depot GitHub.
3. Render lira `render.yaml`.
4. Il creera le site Django, une base PostgreSQL et un disque persistant pour les photos.

Render utilisera:

- Build command: `./build.sh`
- Start command: `python -m gunicorn livret.asgi:application -k uvicorn.workers.UvicornWorker`
- Python: `3.13.5`, defini dans `.python-version`
- Web service: plan `starter`
- PostgreSQL: plan `basic-256mb`
- Photos/media: disque persistant monte sur `/var/data`

## 3. Domaine Namecheap

Dans Render:

1. Ouvre ton service `seake-journal`.
2. Va dans Settings > Custom Domains.
3. Ajoute ton domaine, par exemple `seakejournal.com`.
4. Render ajoutera aussi `www.seakejournal.com`.

Dans Namecheap > Advanced DNS:

1. Supprime les anciens records `A`, `AAAA`, `CNAME` ou URL Redirect qui entrent en conflit.
2. Ajoute un record `A`:
   - Type: `A Record`
   - Host: `@`
   - Value: `216.24.57.1`
   - TTL: `1 min` ou `Automatic`
3. Ajoute un record `CNAME`:
   - Type: `CNAME Record`
   - Host: `www`
   - Value: ton adresse Render, exemple `seake-journal.onrender.com`
   - TTL: `1 min` ou `Automatic`
4. Retourne dans Render et clique `Verify`.

## 4. Variables importantes

Render configure automatiquement:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEBUG=False`
- `MEDIA_ROOT=/var/data/media`

Si tu utilises ton domaine, ajoute dans Render une variable:

```text
ALLOWED_HOSTS=seakejournal.com,www.seakejournal.com
CSRF_TRUSTED_ORIGINS=https://seakejournal.com,https://www.seakejournal.com
```

Remplace `seakejournal.com` par ton vrai domaine.

## 5. Photos et medias

Les photos ajoutees dans l'admin sont des fichiers `media/`.
Cette configuration utilise un disque persistant Render:

```text
MEDIA_ROOT=/var/data/media
```

Le disque est defini dans `render.yaml` avec:

```yaml
disk:
  name: seake-media
  mountPath: /var/data
  sizeGB: 1
```

Comme le disque est attache a un seul service, evite de mettre plusieurs instances web tant que les photos restent sur ce disque.
