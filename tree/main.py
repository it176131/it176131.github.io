from rich import print
from rich.tree import Tree


def main() -> None:
    """An example tree.

    I copied almost verbatim from the rich.Tree tutorial.
    """
    tree = Tree("Example Tree")
    tree.add("foo")
    tree.add("bar")
    print(tree)


if __name__ == "__main__":
    main()
