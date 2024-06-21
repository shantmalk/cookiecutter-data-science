# src/module.py

"""Basic module

A short description of the module.

A set of examples of the module

Examples:
    >>> print("hello world")
    hello world

The following methods are part of this module:

- `main(reports_path)` - Returns some report.
"""

from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.module_name }}.config import REPORTS_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    reports_path: Path = REPORTS_DIR / "labels.csv",
    # -----------------------------------------
):
    '''A basic function that does something that needs to be logged.

    Examples:
        >>> main()
        ...
        >>> main("some/specific/file.csv")
        ...

    Args:
        reports_path (Path, optional): File to write report to. Defaults to REPORTS_DIR/"labels.csv".
    '''

    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Do something here...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
