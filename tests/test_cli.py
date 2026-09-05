import pytest

from iris.cli import build_parser, detect_requested_lang, main


def test_build_parser_uses_spanish_help_text():
    help_text = build_parser(lang="es").format_help()

    assert "Convierte imágenes a WebP" in help_text
    assert "Carpeta de origen" in help_text
    assert "Calidad WebP" in help_text
    assert "Idioma: es, en, pt" in help_text


def test_build_parser_uses_portuguese_help_text():
    help_text = build_parser(lang="pt").format_help()

    assert "Converte imagens para WebP" in help_text
    assert "Pasta de origem" in help_text
    assert "Qualidade WebP" in help_text


def test_detect_requested_lang_defaults_unknown_values_to_english():
    assert detect_requested_lang(["--lang", "unknown"]) == "en"
    assert detect_requested_lang([]) == "en"


def test_main_help_honors_lang_argument(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--lang", "es", "--help"])

    assert exc_info.value.code == 0
    assert "Carpeta de origen" in capsys.readouterr().out


def test_main_quality_validation_uses_requested_language(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--lang", "es", "--quality", "101"])

    assert exc_info.value.code == 2
    assert "--quality debe estar entre 0 y 100" in capsys.readouterr().err


def test_main_workers_validation_uses_requested_language(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--lang", "pt", "--workers", "0"])

    assert exc_info.value.code == 2
    assert "--workers deve ser pelo menos 1" in capsys.readouterr().err
