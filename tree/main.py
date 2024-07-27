"""Contents of tree/main.py"""

from pathlib import Path

from rich import print
from rich.tree import Tree
import typer

app = typer.Typer()


def main(
        directory: Path = typer.Argument(
            help="Directory path to represent as a tree."
        ),
) -> None:
    """Represent a path as a tree."""
    root = directory.cwd().as_posix()
    tree = Tree(root)
    for path in directory.iterdir():
        branch = path.as_posix()
        tree.add(branch)

    print(tree)


if __name__ == "__main__":
    typer.run(main)
