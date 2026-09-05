from pathlib import Path

import pytest
from PIL import Image

import iris


def test_format_bytes_uses_human_readable_units():
    assert iris.format_bytes(0) == "0.0 B"
    assert iris.format_bytes(1024) == "1.0 KB"
    assert iris.format_bytes(1536) == "1.5 KB"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("es", "es"),
        ("Español", "es"),
        ("english", "en"),
        ("pt-br", "pt"),
        ("unknown", "en"),
    ],
)
def test_resolve_lang_normalizes_supported_languages(raw, expected):
    assert iris.resolve_lang(raw) == expected


def test_no_images_does_not_create_output_directory(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    exit_code = iris.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        lang="en",
    )

    assert exit_code == 1
    assert not output_dir.exists()


def test_dry_run_does_not_create_output_directory(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    Image.new("RGB", (2, 2), color="red").save(input_dir / "sample.png")

    exit_code = iris.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        dry_run=True,
        lang="en",
    )

    assert exit_code == 0
    assert not output_dir.exists()
