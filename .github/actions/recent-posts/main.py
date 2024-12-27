from datetime import datetime
from os import environ
from typing import Final

import httpx
from httpx import Response
from pydantic.networks import HttpUrl
from pydantic_xml.model import (
    attr, BaseXmlModel, computed_element, element, wrapped
)
from rich.console import Console

BLOG_URL = "https://it176131.github.io"
NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


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


if __name__ == "__main__":
    resp: Response = httpx.get(url=f"{BLOG_URL}/feed.xml")
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    json_string = model.model_dump_json()
    environ["GITHUB_OUTPUT"] = json_string
    print(environ["GITHUB_OUTPUT"])
