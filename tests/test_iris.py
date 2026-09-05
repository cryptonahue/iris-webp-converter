import pytest
from PIL import Image

import iris.converter as converter


class FixedDatetime:
    @staticmethod
    def now():
        return FixedDatetime()

    def strftime(self, _format):
        return "20240101_010203"


def test_format_bytes_uses_human_readable_units():
    assert converter.format_bytes(0) == "0.0 B"
    assert converter.format_bytes(1024) == "1.0 KB"
    assert converter.format_bytes(1536) == "1.5 KB"


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
    assert converter.resolve_lang(raw) == expected


def test_no_images_does_not_create_output_directory(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    exit_code = converter.convert_to_webp(
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

    exit_code = converter.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        dry_run=True,
        lang="en",
    )

    assert exit_code == 0
    assert not output_dir.exists()


def test_converts_png_to_webp(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    Image.new("RGB", (3, 2), color="blue").save(input_dir / "sample.png")

    exit_code = converter.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        lang="en",
    )

    assert exit_code == 0
    [conversion_dir] = output_dir.iterdir()
    output_file = conversion_dir / "sample.webp"
    assert output_file.exists()
    with Image.open(output_file) as converted:
        assert converted.format == "WEBP"
        assert converted.size == (3, 2)


def test_preserves_nested_folder_structure(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    nested_dir = input_dir / "gallery" / "summer"
    nested_dir.mkdir(parents=True)
    Image.new("RGB", (1, 1), color="green").save(nested_dir / "photo.jpg")

    exit_code = converter.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        lang="en",
    )

    assert exit_code == 0
    [conversion_dir] = output_dir.iterdir()
    assert (conversion_dir / "gallery" / "summer" / "photo.webp").exists()


def test_skip_existing_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    Image.new("RGB", (2, 2), color="red").save(input_dir / "sample.png")

    monkeypatch.setattr(converter, "datetime", FixedDatetime)
    monkeypatch.setattr(converter.uuid, "uuid4", lambda: "12345678-0000-0000-0000-000000000000")
    existing_file = output_dir / "webp_conversion_20240101_010203_12345678" / "sample.webp"
    existing_file.parent.mkdir(parents=True)
    existing_file.write_bytes(b"existing")

    exit_code = converter.convert_to_webp(
        input_folder=input_dir,
        output_folder=output_dir,
        skip_existing=True,
        lang="en",
    )

    assert exit_code == 0
    assert existing_file.read_bytes() == b"existing"
