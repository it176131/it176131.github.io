from datetime import datetime
from os import environ
import subprocess
from typing import Annotated, Final

import httpx
from httpx import Response
from pydantic.networks import HttpUrl
from pydantic.types import FilePath
from pydantic_xml.model import (
    attr, BaseXmlModel, computed_element, element, wrapped
)
from typer import Typer
from typer.params import Argument

BLOG_URL = "https://it176131.github.io"
NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}
app = Typer()


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    """A blog post entry from the RSS feed."""

    title: str = element()
    relative_url: str = wrapped(path="link", entity=attr(name="href"))
    published: datetime = element()
    updated: datetime = element()
    author: str = wrapped(path="author/name")

    @computed_element
    def link(self: "Entry") -> HttpUrl:
        """Resolve <entry.link[href]> to full URL."""
        return HttpUrl(url=f"{BLOG_URL}{self.relative_url}")


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
    """Validate the RSS feed/XML from my blog."""

    # We limit to the first <entry> from the RSS feed as it is the most
    # recently published.
    entry: Entry


@app.command()
def main(
        readme: Annotated[
            FilePath,
            Argument(help="Path to file where metadata will be written.")
        ] = "README.md"
) -> None:
    """Write most recent blog post metadata to ``readme``."""
    resp: Response = httpx.get(url=f"{BLOG_URL}/feed.xml")
    xml: bytes = resp.content
    model = Feed.from_xml(source=xml)
    json_string = model.model_dump_json()
    with open(environ["GITHUB_OUTPUT"], mode="a") as f:
        f.write(f"result={json_string}")

    with readme.open(mode="a") as f:
        f.write(f"result={json_string}\n")

    subprocess.run(args=["git", "config", "--global", "user.email", "it176131-github-io-bot@example.com"])
    subprocess.run(args=["git", "config", "--global", "user.name", "it176131-github-io-bot"])
    subprocess.run(args=["git", "add", readme.as_posix()])
    subprocess.run(args=["git", "commit", "-m", "Synced and updated with most recent it176131.github.io blog post"])
    subprocess.run(args=["git", "push"])
    print("Success?")


if __name__ == "__main__":
    app()
