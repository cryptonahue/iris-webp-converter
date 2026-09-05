import io
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from PIL import Image

from iris.translations import text

if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        with suppress(Exception):
            stream.reconfigure(encoding="utf-8", errors="replace")

try:
    import cairosvg

    HAS_CAIROSVG = True
except Exception:
    HAS_CAIROSVG = False

SUPPORTED_LANGS = {
    "es": "es",
    "español": "es",
    "spanish": "es",
    "en": "en",
    "english": "en",
    "inglés": "en",
    "ingles": "en",
    "pt": "pt",
    "pt-br": "pt",
    "pt_br": "pt",
    "brasil": "pt",
    "brazilian": "pt",
}

SUPPORTED_FORMATS = {".svg", ".jpg", ".jpeg", ".png"}


def resolve_lang(value):
    """Normalize --lang values to es/en/pt, defaulting to English."""
    return SUPPORTED_LANGS.get(str(value).strip().lower(), "en")


def format_bytes(size: float) -> str:
    """Convert bytes to a human-readable size."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def build_output_path(output_folder):
    """Build the unique output folder path for a conversion run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return Path(output_folder) / f"webp_conversion_{timestamp}_{unique_id}"


def discover_image_files(input_path, output_path, quality, skip_existing):
    """Find supported images and map each one to its WebP destination."""
    image_files = []
    for file_path in input_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            relative = file_path.relative_to(input_path)
            dest = output_path / relative.parent / f"{file_path.stem}.webp"
            image_files.append((str(file_path), str(dest), quality, skip_existing))
    return image_files


def convert_single_image(args):
    """Convert a single image to WebP and return a result dictionary."""
    file_path, output_file_path, quality, skip_existing = args

    try:
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1].lower()

        if skip_existing and os.path.exists(output_file_path):
            return {
                "filename": filename,
                "relative_path": file_path,
                "success": True,
                "skipped": True,
            }

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        original_size = os.path.getsize(file_path)

        if file_ext == ".svg":
            if not HAS_CAIROSVG:
                return {
                    "filename": filename,
                    "success": False,
                    "error": "cairosvg is required for SVG. Install: pip install cairosvg",
                }
            png_data = cairosvg.svg2png(url=file_path)
            image = Image.open(io.BytesIO(png_data))
        else:
            image = Image.open(file_path)

        image = image.convert("RGBA" if image.mode in ("RGBA", "LA", "P") else "RGB")

        image.save(output_file_path, "WebP", quality=quality)
        new_size = os.path.getsize(output_file_path)

        return {
            "filename": filename,
            "output_filename": os.path.basename(output_file_path),
            "relative_path": file_path,
            "original_size": original_size,
            "new_size": new_size,
            "size_reduction": (
                ((original_size - new_size) / original_size) * 100 if original_size else 0
            ),
            "dimensions": f"{image.width}x{image.height}",
            "success": True,
            "skipped": False,
        }
    except Exception as exc:
        return {"filename": os.path.basename(file_path), "success": False, "error": str(exc)}


def convert_to_webp(
    input_folder="input",
    output_folder="output",
    quality=85,
    max_workers=4,
    dry_run=False,
    skip_existing=False,
    lang="en",
):
    """Find images recursively and convert them to WebP."""
    input_path = Path(input_folder).resolve()
    if not input_path.exists() or not input_path.is_dir():
        print(text(lang, "input_missing", folder=input_folder))
        return 1

    output_path = build_output_path(output_folder)
    image_files = discover_image_files(input_path, output_path, quality, skip_existing)

    if not image_files:
        print(text(lang, "no_images", folder=input_folder))
        print(text(lang, "formats", formats=", ".join(sorted(SUPPORTED_FORMATS))))
        return 1

    if not dry_run:
        output_path.mkdir(parents=True, exist_ok=True)

    print(text(lang, "starting"))
    print(text(lang, "input", path=input_path))
    print(text(lang, "output", path=output_path))
    print(text(lang, "images_found", count=len(image_files)))
    print(text(lang, "quality", quality=quality))
    print(text(lang, "workers", workers=max_workers))
    if dry_run:
        print(text(lang, "dry_run_mode"))

    results = []
    total_original = 0
    total_new = 0

    if dry_run:
        for _, dest, _, _ in image_files:
            print(text(lang, "dry_sim", name=Path(dest).name))
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(convert_single_image, args): args[0] for args in image_files}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                if result.get("success") and not result.get("skipped"):
                    if result.get("original_size") is not None:
                        total_original += result["original_size"]
                        total_new += result["new_size"]
                        rel = Path(result["relative_path"]).relative_to(input_path)
                        print(text(lang, "ok", rel=rel, out=result["output_filename"]))
                        print(
                            text(
                                lang,
                                "dims",
                                dims=result["dimensions"],
                                os=format_bytes(result["original_size"]),
                                ns=format_bytes(result["new_size"]),
                                red=result["size_reduction"],
                            )
                        )
                elif result.get("skipped"):
                    print(text(lang, "skipped", name=result["filename"]))
                else:
                    print(text(lang, "failed", name=result["filename"], error=result["error"]))

    successful = len([r for r in results if r.get("success") and not r.get("skipped")])
    skipped = len([r for r in results if r.get("skipped")])
    failed = len([r for r in results if not r.get("success")])

    print("\n" + "=" * 60)
    print(text(lang, "summary_title"))
    print("=" * 60)
    if dry_run:
        print(text(lang, "dry_summary", count=len(image_files)))
    else:
        print(text(lang, "converted", count=successful))
        print(text(lang, "skipped_count", count=skipped))
        print(text(lang, "failed_count", count=failed))
        if total_original > 0:
            reduction = ((total_original - total_new) / total_original) * 100
            print(text(lang, "sizes", os=format_bytes(total_original), ns=format_bytes(total_new)))
            print(text(lang, "reduction", red=reduction))
    print(text(lang, "output", path=output_path))
    print("=" * 60)
    return 0
