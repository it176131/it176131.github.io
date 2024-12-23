# from datetime import datetime
# from typing import Final
#
# import httpx
# from httpx import Response
# from pydantic_xml.model import BaseXmlModel, element, wrapped
# from rich.console import Console
#
# NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}
#
#
# class Author(BaseXmlModel, tag="author", nsmap=NSMAP):
#     """A blog post author from the RSS feed."""
#
#     name: str = element(tag="name")
#
#
# class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
#     """A blog post entry from the RSS feed."""
#
#     title: str = element()
#     published: datetime = element()
#     updated: datetime = element()
#     author: Author
#     # author: str = wrapped(path="author", entity=element(tag="name"))
#     # author: str = wrapped(path="author/name")
#
#
# class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
#
#     """Validate the RSS feed/XML from my blog."""
#
#     entries: list[Entry] = element()
#
#
# if __name__ == "__main__":
#     BLOG_URL = "https://it176131.github.io/feed.xml"
#     resp: Response = httpx.get(url=BLOG_URL)
#     xml: bytes = resp.content
#     # with open("blog.xml", mode="rb") as f:
#     #     xml: bytes = f.read()
#     #
#     console = Console()
#     model = Feed.from_xml(source=xml)
#     console.print(model)

from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


# NOTE -- we have to declare the _same_ `nsmap` for our `Entry` class as
# we did in the `Feed` class, otherwise we'll run into the same errors
# from before.
class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP):
    """A blog post entry from the RSS feed."""

    ...


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
    """Validate the RSS feed/XML from my blog."""

    entry: Entry

if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)