"""Contents of tree/main.py"""

from pathlib import Path
from typing import Annotated

from rich import print
from rich.tree import Tree
import typer

app = typer.Typer()


def grow_tree(path: Path, tree: Tree, show_private) -> None:
    """Grow the ``tree`` recursively."""
    for p in path.iterdir():
        if not show_private and p.name.startswith("."):
            continue

        branch: Tree = tree.add(p.name)
        if p.is_dir():
            grow_tree(path=p, tree=branch, show_private=show_private)


def main(
        directory: str = typer.Argument(
            help="Directory path to represent as a tree."
        ),
        show_private: Annotated[
            bool,
            typer.Option(
                "--all/", "-a", help="Show all files."
            ),
        ] = False
) -> None:
    """Represent a path as a tree."""
    tree = Tree(directory)
    root = Path(directory)
    grow_tree(path=root, tree=tree, show_private=show_private)
    print(tree)


if __name__ == "__main__":
    typer.run(main)
