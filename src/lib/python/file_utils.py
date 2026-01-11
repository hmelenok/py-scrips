"""File utilities for handling project paths."""

import os
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def get_data_path(subdir, filename):
    """Get path to data file.

    Args:
        subdir: Subdirectory under data/ (e.g., 'config', 'reference-data', 'raw-data')
        filename: Name of the file

    Returns:
        Path object to the data file
    """
    return get_project_root() / "data" / subdir / filename


def get_output_path(subdir, filename):
    """Get path to output file.

    Args:
        subdir: Subdirectory under output/ (e.g., 'csv', 'images', 'logs', 'text')
        filename: Name of the file

    Returns:
        Path object to the output file
    """
    return get_project_root() / "output" / subdir / filename


def ensure_dir(path):
    """Ensure directory exists.

    Args:
        path: Path to directory (string or Path object)
    """
    os.makedirs(path, exist_ok=True)
