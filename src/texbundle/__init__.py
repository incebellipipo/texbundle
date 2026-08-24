from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("texbundle")
except PackageNotFoundError:  # pragma: no cover - not installed
    __version__ = "0.0.0"

from .bundle import main

__all__ = ["main", "__version__"]
