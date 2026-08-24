# texbundle

Zip only the files actually needed to build a LaTeX PDF.

`texbundle` compiles your document once with `-recorder`, which makes LaTeX
write a `.fls` file listing every path it opened. Everything under your
project root that was actually used gets bundled; TeX distribution files and
build artifacts (`.aux`, `.log`, `.out`, ...) do not. Handy for submitting a
clean source archive to arXiv, a journal, or a co-author.

## Install

```sh
pip install texbundle
```

Requires Python 3.9+ and a LaTeX toolchain on `PATH` (`latexmk` if available,
otherwise `pdflatex`/`xelatex`/`lualatex` directly). No other dependencies.

## Usage

```sh
texbundle                          # main.tex -> bundle.zip
texbundle paper.tex -o submit.zip
texbundle thesis.tex -e xelatex --include-pdf
texbundle main.tex --skip-build --dry-run
```

Run it from your project root, next to your main `.tex` file.

### Options

| Flag | Description |
| --- | --- |
| `main` | Main `.tex` file to build (default: `main.tex`) |
| `-o, --out` | Output archive path (default: `bundle.zip`) |
| `-e, --engine` | `pdflatex` (default), `xelatex`, or `lualatex` |
| `--include-pdf` | Also add the compiled PDF to the archive |
| `--skip-build` | Reuse an existing `.fls` instead of recompiling |
| `--dry-run` | List the files that would be bundled, without writing an archive |
| `--version` | Print the installed version and exit |

## License

[EUPL-1.2](https://interoperable-europe.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
