from __future__ import annotations

import logging
import os
import sys
import warnings
from pathlib import Path


def setup_pipeline_logging(project_root: Path, *, console_level: int = logging.INFO) -> logging.Logger:
    """
    Configure root logging: DEBUG to file, INFO (default) to stdout.
    Warnings are captured and written through the logging system for review in logs/pipeline.log.
    """
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "pipeline.log"

    logging.captureWarnings(True)

    debug_env = os.environ.get("PERO_DEBUG", "").strip().lower() in ("1", "true", "yes")
    file_level = logging.DEBUG if debug_env else logging.INFO

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG if debug_env else logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(console_level)
    stream_handler.setFormatter(fmt)

    root.addHandler(file_handler)
    root.addHandler(stream_handler)

    logging.getLogger("py.warnings").setLevel(logging.WARNING)
    for noisy in (
        "PIL",
        "PIL.PngImagePlugin",
        "matplotlib",
        "matplotlib.font_manager",
        "fontTools",
        "fontTools.subset",
    ):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    try:
        from sklearn.exceptions import ConvergenceWarning

        warnings.filterwarnings("ignore", category=ConvergenceWarning)
    except Exception:
        pass

    warnings.filterwarnings(
        "ignore",
        message="X does not have valid feature names, but .* was fitted with feature names",
        category=UserWarning,
    )

    # Seaborn may warn on singular KDE when a column is nearly constant; safe to ignore for these plots.
    warnings.filterwarnings(
        "ignore",
        message="Dataset has 0 variance; skipping density estimate.*",
        category=UserWarning,
        module="seaborn.distributions",
    )

    log = logging.getLogger("pero.pipeline")
    log.info("Logging initialized; file=%s file_level=%s PERO_DEBUG=%s", log_path, logging.getLevelName(file_level), debug_env)
    return log


def configure_matplotlib_backends() -> None:
    """Reduce noisy backend or layout warnings in script runs."""
    warnings.filterwarnings(
        "ignore",
        message="FigureCanvasAgg is non-interactive, and thus cannot be shown",
        category=UserWarning,
    )
    warnings.filterwarnings(
        "ignore",
        message="This figure includes Axes that are not compatible with tight_layout",
        category=UserWarning,
    )
