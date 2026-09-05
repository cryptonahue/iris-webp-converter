import pytest

from iris.cli import build_parser, main


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


def test_main_help_honors_lang_argument(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--lang", "es", "--help"])

    assert exc_info.value.code == 0
    assert "Carpeta de origen" in capsys.readouterr().out
