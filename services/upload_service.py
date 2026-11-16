import os
from pathlib import Path
from uuid import uuid4

from PIL import Image
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def save_image(image_file, upload_folder):
    if not image_file or not image_file.filename:
        return None

    extension = Path(image_file.filename).suffix.lower().lstrip('.')
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError('Please upload a PNG, JPG, JPEG, GIF, or WEBP image.')

    safe_stem = secure_filename(Path(image_file.filename).stem) or 'image'
    filename = f'{safe_stem}-{uuid4().hex}.{extension}'
    folder = Path(upload_folder)
    folder.mkdir(parents=True, exist_ok=True)
    original_path = folder / filename
    thumbnail_path = folder / f'{original_path.stem}_thumb{original_path.suffix}'

    image_file.save(original_path)
    try:
        with Image.open(original_path) as image:
            image.load()
            width, height = image.size
            thumbnail = image.copy()
            thumbnail = thumbnail.resize(
                (max(1, width // 2), max(1, height // 2)),
                Image.Resampling.LANCZOS,
            )
            if thumbnail.mode not in ('RGB', 'RGBA'):
                thumbnail = thumbnail.convert('RGB')
            thumbnail.save(thumbnail_path)
    except Exception:
        original_path.unlink(missing_ok=True)
        thumbnail_path.unlink(missing_ok=True)
        raise ValueError('The uploaded file is not a valid image.')

    return {
        'original': filename,
        'thumbnail': thumbnail_path.name,
        'original_url': f'/static/uploads/{filename}',
        'thumbnail_url': f'/static/uploads/{thumbnail_path.name}',
    }
