"""Contents of tree/main.py"""

from pathlib import Path
from typing import Annotated

from rich import print
from rich.tree import Tree
import typer

app = typer.Typer()


def main(
        directory: Path = typer.Argument(
            help="Directory path to represent as a tree."
        ),
        all: Annotated[
            bool,
            typer.Option(
                "--all/", "-a", help="Show all files."
            ),
        ] = False
) -> None:
    """Represent a path as a tree."""
    root = directory.cwd().as_posix()
    tree = Tree(root)
    for path in directory.iterdir():
        if not all and path.name.startswith("."):
            continue

        branch = path.as_posix()
        tree.add(branch)

    print(tree)


if __name__ == "__main__":
    typer.run(main)
