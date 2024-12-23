from datetime import datetime
from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel, element, wrapped
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


class Author(BaseXmlModel, tag="author", nsmap=NSMAP):

    name: str = element(tag="name")


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    """A blog post XML entry from the RSS feed."""

    # NOTE -- I'm validating some of the entry subfields to
    # differentiate from other entries.
    title: str = element()
    published: datetime = element()
    updated: datetime = element()
    # author: Author
    # # author: str = wrapped(path="author", entity=element(tag="name"))
    # author: str = wrapped(path="author/name")


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

    # generator: dict[str, str] = element(repr=False)
    # # link_self: dict[str, str] = element(tag="link")
    # # link_alt: dict[str, str] = element(tag="link")
    # links: list[dict[str, str]] = element(tag="link", exclude=True)
    # updated: datetime = element()
    # id: str = element(exclude=True)
    # title: str = element(exclude=True)
    # subtitle: str = element(exclude=True)
    # author: Author = element(exclude=True)
    # # author: str = wrapped(path="author", entity=element(tag="name"))
    # # author: str = wrapped(path="author/name")
    # entry1: Entry
    # entry2: Entry
    entries: list[Entry] = element()


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    # with open("blog.xml", mode="rb") as f:
    #     xml: bytes = f.read()
    #
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)
