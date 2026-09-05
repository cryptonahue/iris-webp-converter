import argparse

from iris.converter import convert_to_webp, resolve_lang
from iris.translations import text


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="iris",
        description="Iris: WebP Image Converter",
    )
    parser.add_argument(
        "--input",
        "-i",
        default="input",
        help="Source folder (default: input)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="Destination folder (default: output)",
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=85,
        help="WebP quality 0-100 (default: 85)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Parallel workers (default: 4)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate conversion without creating files",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip already converted files",
    )
    parser.add_argument(
        "--lang",
        "-l",
        default="en",
        help="Language: es, en, pt (default: en)",
    )

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
