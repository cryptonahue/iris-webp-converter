import argparse

from iris.converter import convert_to_webp, resolve_lang
from iris.translations import text


def build_parser(lang="en"):
    parser = argparse.ArgumentParser(
        prog="iris",
        description=text(lang, "desc"),
    )
    parser.add_argument(
        "--input",
        "-i",
        default="input",
        help=text(lang, "input_help"),
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help=text(lang, "output_help"),
    )
    parser.add_argument(
        "--quality",
        "-q",
        type=int,
        default=85,
        help=text(lang, "quality_help"),
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help=text(lang, "workers_help"),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=text(lang, "dry_run_help"),
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=text(lang, "skip_existing_help"),
    )
    parser.add_argument(
        "--lang",
        "-l",
        default="en",
        help=text(lang, "lang_help"),
    )
    return parser


def detect_requested_lang(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--lang", "-l", default="en")
    args, _unknown = parser.parse_known_args(argv)
    return resolve_lang(args.lang)


def main(argv=None):
    lang = detect_requested_lang(argv)
    parser = build_parser(lang)
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
