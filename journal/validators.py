from django.core.exceptions import ValidationError


IMAGE_MAX_BYTES = 15 * 1024 * 1024
VIDEO_MAX_BYTES = 100 * 1024 * 1024
PDF_MAX_BYTES = 50 * 1024 * 1024


def _header(uploaded_file, length=32):
    position = uploaded_file.tell()
    uploaded_file.seek(0)
    value = uploaded_file.read(length)
    uploaded_file.seek(position)
    return value


def _validate_size(uploaded_file, maximum, label):
    if uploaded_file.size > maximum:
        maximum_mb = maximum // (1024 * 1024)
        raise ValidationError(f"Le {label} ne doit pas depasser {maximum_mb} Mo.")


def validate_image_file(uploaded_file):
    _validate_size(uploaded_file, IMAGE_MAX_BYTES, "fichier image")
    header = _header(uploaded_file)
    is_image = any(
        (
            header.startswith(b"\xff\xd8\xff"),
            header.startswith(b"\x89PNG\r\n\x1a\n"),
            header.startswith((b"GIF87a", b"GIF89a")),
            header.startswith(b"RIFF") and header[8:12] == b"WEBP",
            header[4:8] == b"ftyp" and header[8:12] in {b"avif", b"avis"},
        )
    )
    if not is_image:
        raise ValidationError("Le contenu du fichier ne correspond pas a une image acceptee.")


def validate_video_file(uploaded_file):
    _validate_size(uploaded_file, VIDEO_MAX_BYTES, "fichier video")
    header = _header(uploaded_file)
    is_video = header.startswith(b"\x1aE\xdf\xa3") or header[4:8] == b"ftyp"
    if not is_video:
        raise ValidationError("Le contenu du fichier ne correspond pas a une video acceptee.")


def validate_pdf_file(uploaded_file):
    _validate_size(uploaded_file, PDF_MAX_BYTES, "fichier PDF")
    if not _header(uploaded_file).startswith(b"%PDF-"):
        raise ValidationError("Le contenu du fichier ne correspond pas a un PDF.")
