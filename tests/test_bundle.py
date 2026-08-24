from __future__ import annotations

import sys
import zipfile

import pytest

from texbundle.bundle import parse_fls, write_zip


def _write(path, content=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_parse_fls_filters_skip_suffixes_dedupes_and_stays_in_root(tmp_path):
    root = tmp_path / "proj"
    kept_tex = _write(root / "main.tex", "\\documentclass{article}")
    kept_img = _write(root / "figs" / "plot.png", "binary")
    skipped_aux = _write(root / "main.aux", "")
    outside = _write(tmp_path / "outside" / "shared.sty", "")
    missing = root / "does-not-exist.tex"

    fls = root / "main.fls"
    fls.write_text(
        "PWD {}\n"
        "INPUT main.tex\n"
        "INPUT main.tex\n"
        "INPUT figs/plot.png\n"
        "INPUT main.aux\n"
        "INPUT MAIN.AUX\n"
        "INPUT {}\n"
        "INPUT {}\n".format(root, outside, missing),
        encoding="utf-8",
    )

    files = parse_fls(fls, root)

    assert kept_tex in files
    assert kept_img in files
    assert skipped_aux not in files
    assert outside not in files
    assert missing not in files
    # main.tex was listed twice; it should only appear once.
    assert files.count(kept_tex) == 1


def test_write_zip_uses_posix_relative_paths(tmp_path):
    root = tmp_path / "proj"
    a = _write(root / "main.tex", "content-a")
    b = _write(root / "sub" / "chapter.tex", "content-b")
    out = tmp_path / "bundle.zip"

    write_zip([a, b], root, out)

    with zipfile.ZipFile(out) as zf:
        names = sorted(zf.namelist())
        assert names == ["main.tex", "sub/chapter.tex"]
        assert zf.read("main.tex") == b"content-a"


def test_cli_version_flag(capsys):
    from texbundle.bundle import main

    old_argv = sys.argv
    sys.argv = ["texbundle", "--version"]
    try:
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
    finally:
        sys.argv = old_argv

    out = capsys.readouterr().out
    assert "texbundle" in out


def test_cli_missing_file_returns_error_string(tmp_path, monkeypatch):
    from texbundle.bundle import main

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["texbundle", "missing.tex"])

    result = main()

    assert isinstance(result, str)
    assert "missing.tex" in result
