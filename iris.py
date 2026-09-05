#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iris — WebP Image Converter

Convierte imágenes (SVG, JPG, JPEG, PNG) a WebP con procesamiento
en paralelo, preservando la estructura de carpetas original.
Idiomas soportados: español (es), inglés (en), portugués de Brasil (pt).

Uso:
    python iris.py
    python iris.py --input ./fotos --quality 90 --lang en
    python iris.py --input ./fotos --output ./out --workers 8 --dry-run
"""

import argparse
import io
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from PIL import Image

# Forzar UTF-8 en consolas Windows para poder mostrar emojis/acentos
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

try:
    import cairosvg  # solo necesario para convertir SVG
    HAS_CAIROSVG = True
except Exception:  # ImportError u OSError (librería nativa cairo ausente)
    HAS_CAIROSVG = False

from translations import text  # noqa: E402

SUPPORTED_LANGS = {
    "es": "es", "español": "es", "spanish": "es",
    "en": "en", "english": "en", "inglés": "en", "ingles": "en",
    "pt": "pt", "pt-br": "pt", "pt_br": "pt", "brasil": "pt", "brazilian": "pt",
}

SUPPORTED_FORMATS = {".svg", ".jpg", ".jpeg", ".png"}


def resolve_lang(value):
    """Normaliza el valor --lang a es/en/pt (por defecto inglés)."""
    return SUPPORTED_LANGS.get(str(value).strip().lower(), "en")


def format_bytes(size: float) -> str:
    """Convierte bytes a formato legible."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def convert_single_image(args):
    """Convierte una única imagen a WebP. Devuelve un dict con el resultado."""
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
                    "error": "cairosvg requerido para SVG. Instala: pip install cairosvg",
                }
            png_data = cairosvg.svg2png(url=file_path)
            image = Image.open(io.BytesIO(png_data))
        else:
            image = Image.open(file_path)

        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGBA")
        else:
            image = image.convert("RGB")

        image.save(output_file_path, "WebP", quality=quality)
        new_size = os.path.getsize(output_file_path)

        return {
            "filename": filename,
            "output_filename": os.path.basename(output_file_path),
            "relative_path": file_path,
            "original_size": original_size,
            "new_size": new_size,
            "size_reduction": ((original_size - new_size) / original_size) * 100 if original_size else 0,
            "dimensions": f"{image.width}x{image.height}",
            "success": True,
            "skipped": False,
        }
    except Exception as e:
        return {"filename": os.path.basename(file_path), "success": False, "error": str(e)}


def convert_to_webp(input_folder="input", output_folder="output",
                    quality=85, max_workers=4, dry_run=False, skip_existing=False,
                    lang="en"):
    """Busca imágenes recursivamente y las convierte a WebP."""
    input_path = Path(input_folder).resolve()
    if not input_path.exists() or not input_path.is_dir():
        print(text(lang, "input_missing", folder=input_folder))
        return 1

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    output_path = Path(output_folder) / f"webp_conversion_{timestamp}_{unique_id}"

    image_files = []
    for file_path in input_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            relative = file_path.relative_to(input_path)
            dest = output_path / relative.parent / f"{file_path.stem}.webp"
            image_files.append((str(file_path), str(dest), quality, skip_existing))

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
                        print(text(lang, "dims", dims=result["dimensions"],
                                    os=format_bytes(result["original_size"]),
                                    ns=format_bytes(result["new_size"]),
                                    red=result["size_reduction"]))
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="iris",
        description="Iris: WebP Image Converter",
    )
    parser.add_argument("--input", "-i", default="input",
                        help="Source folder (default: input)")
    parser.add_argument("--output", "-o", default="output",
                        help="Destination folder (default: output)")
    parser.add_argument("--quality", "-q", type=int, default=85,
                        help="WebP quality 0-100 (default: 85)")
    parser.add_argument("--workers", "-w", type=int, default=4,
                        help="Parallel workers (default: 4)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate conversion without creating files")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip already converted files")
    parser.add_argument("--lang", "-l", default="en",
                        help="Language: es, en, pt (default: en)")

    args = parser.parse_args(argv)
    lang = resolve_lang(args.lang)

    if not (0 <= args.quality <= 100):
        parser.error(text(lang, "quality_range_err"))
    if args.workers < 1:
        parser.error(text(lang, "workers_min_err"))

    return convert_to_webp(
        input_folder=args.input,
        output_folder=args.output,
        quality=args.quality,
        max_workers=args.workers,
        dry_run=args.dry_run,
        skip_existing=args.skip_existing,
        lang=lang,
    )


if __name__ == "__main__":
    sys.exit(main())

