---
layout: "post"
title: "pydantic-xml: Parsing My RSS Feed"
date: 2024-12-22
---

I thought
it'd be cool
to add my most recent blog post to my [GitHub profile](https://github.com/it176131)
using a custom GitHub action and workflow.
To do that, I'd need to know which post was most recently published along with its title, URL, etc.
After looking at the [GoodReads workflow](https://github.com/it176131/it176131/blob/dev/.github/workflows/goodreads-books-workflow.yml) on my profile,
I figured I could get that information from my blog's RSS feed.

> [RSS](https://en.wikipedia.org/wiki/RSS) is a web feed that allows users and applications to access updates to websites in a standardized,
> computer-readable format.
> 
> —Wikipedia

Accessing my blog's RSS feed is as simple as adding _/feed.xml_ to the end of its URL.
Check it out here 👉 [https://it176131.github.io/feed.xml](https://it176131.github.io/feed.xml).
> Why _.xml_ and not _.rss_?
> It turns out that RSS is an extension of XML so in theory we could use either extension.
> However, _.rss_ doesn't work on the URL, so _.xml_ it is.

# pydantic-xml
I mentioned
using [`pydantic`](https://docs.pydantic.dev/latest/) in [a previous post]({{ site.baseurl }}{% link _posts/2024-11-29-dynamic-enums.md %})
for parsing and validating JSON files.
If you explore the library's main page,
you'll hopefully come across a link to the [`awesome-pydantic` repo](https://github.com/Kludex/awesome-pydantic)
which contains a list of projects that use `pydantic`.
Under the [_Utilities_ section](https://github.com/Kludex/awesome-pydantic?tab=readme-ov-file#utilities)
you'll find a package called [`pydantic-xml`](https://github.com/dapper91/pydantic-xml), which extends `pydantic` to allow parsing and validation of XML.

I don't have much experience parsing XML, but I do know how to use `pydantic`.
How hard could it be to transfer my `pydantic` knowledge to `pydantic-xml`?

# XML != JSON
Validating JSON with `pydantic` requires you to define a class, then supply the JSON as an argument.
`pydantic-xml` is similar, but there are some gotchas.

#### Namespaces

> They're for allowing multiple markup languages to be combined,
> without having to worry about conflicts of element and attribute names.
> 
> —[What are XML namespaces for?](https://stackoverflow.com/a/128413/6509519)

The first couple of lines in my blog's XML look like this:
```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    ...
</feed>
```

Based on what I saw in the [`pydantic-xml` Quickstart](https://pydantic-xml.readthedocs.io/en/stable/pages/quickstart.html#),
I'd expect the model class to be defined like so:
```python
import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel
from rich.console import Console


class Feed(BaseXmlModel):
    """Validate the RSS feed/XML from my blog."""
    
    ...


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```

But no.
This raises the following error:
```python-traceback
pydantic_xml.errors.ParsingError: root element not found (actual: {http://www.w3.org/2005/Atom}feed, expected: Feed)
```

Confused, but not beaten, I read on.
After trying the example code a few times and altering my own XML, I found that I needed to either:
1. make my "F" lowercase in the class definition to match the XML tag name, i.e. `Feed` ➡️ `feed`, or
2. add `tag="feed"` to the `Feed` signature line.

I chose the latter as I prefer uppercased class names.
```diff
import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel
from rich.console import Console


- class Feed(BaseXmlModel):
+ class Feed(BaseXmlModel, tag="feed"):
    """Validate the RSS feed/XML from my blog."""
    
    ...


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```

Running my updated code, I was greeted with another error 😣:
```python-traceback
pydantic_xml.errors.ParsingError: root element not found (actual: {http://www.w3.org/2005/Atom}feed, expected: feed)
```

This one appears identical to the previous,
but with one small difference—the expected value is now "feed" instead of "Feed".
That means adding `tag="feed"` correctly told the underlying parser to look for a "feed" tag,
but for some reason it can't find it.

Looking at the _actual_ tag in the error message,
_{http://www.w3.org/2005/Atom}feed_, I noticed that the URL is assigned to an attribute called `xmlns`,
which stands for _XML namespace_.
Searching for ["namespace" in the `pydantic-xml` docs](https://pydantic-xml.readthedocs.io/en/stable/pages/misc.html#default-namespace), I found the missing link:
I need to include the tag's namespace in my class signature.
```diff
+ from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel
from rich.console import Console

+ NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


- class Feed(BaseXmlModel, tag="feed"):
+ class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP):
    """Validate the RSS feed/XML from my blog."""
    
    ...


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)  # >>> Feed()

```
> [!NOTE]
> 
> The key in the `NSMAP` is an empty string.
> This sets a default namespace for a model and its sub-fields.
> 
> —[pydantic-xml Default namespace](https://pydantic-xml.readthedocs.io/en/stable/pages/misc.html#default-namespace)

That modification allowed me to parse the first couple lines of the XML.
Now to get to my entries.

#### Order Matters
Accessing fields in JSON is similar to interacting with a Python `dict`:
```python
some_dict = {"a": 0, "b": 1}
print(some_dict["b"])  # >>> 0
```
Because of this, you can ignore the fields you don't care about when defining a `pydantic` class:
```python
from pydantic.main import BaseModel


class Model(BaseModel):
    """Demo model."""
    
    b: int


if __name__ == "__main__":
    some_dict = {"a": 0, "b": 1}
    model = Model(**some_dict)
    print(model)  # >>> Model(b=1)

```
This doesn't work (by default) when defining a `pydantic-xml` class.

These are the next few lines in my XML,
from the `<feed>` tag up through the first `<entry>` tag:
> [!NOTE]
>
> The `<content>` and `<summary>` descriptions were shortened for brevity.

```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <generator uri="https://jekyllrb.com/" version="3.10.0">Jekyll</generator>
    <link href="/feed.xml" rel="self" type="application/atom+xml"/>
    <link href="/" rel="alternate" type="text/html"/>
    <updated>2024-12-13T02:39:38+00:00</updated>
    <id>/feed.xml</id>
    <title type="html">My Blog</title>
    <subtitle>Where I write things...</subtitle>
    <author>
        <name>Ian Thompson</name>
    </author>
    <entry>
        <title type="html">isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit</title>
        <link href="/2024/12/12/isort.html" rel="alternate" type="text/html"
              title="isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit"/>
        <published>2024-12-12T00:00:00+00:00</published>
        <updated>2024-12-12T00:00:00+00:00</updated>
        <id>/2024/12/12/isort</id>
        <content type="html" xml:base="/2024/12/12/isort.html">...</content>
        <author>
            <name>Ian Thompson</name>
        </author>
        <summary type="html">...</summary>
    </entry>
    ...
</feed>
```
If I were to define the `Feed.entry` attribute like I would in `pydantic`:
```python
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


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP):
    """Validate the RSS feed/XML from my blog."""
    
    entry: Entry


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
We will raise the following error:
```python-traceback
pydantic_core._pydantic_core.ValidationError: 1 validation error for Feed
entry
  [line -1]: Field required [type=missing, input_value={}, input_type=dict]
```

This is a [`pydantic` `ValidationError`](https://docs.pydantic.dev/latest/errors/validation_errors/)—which I'm quite familiar with—but it's not immediately known
how to fix it,
let alone understand why it was raised.
Through some trial and error,
I found that adding an attribute for the first element after `<feed>`, i.e.,
`<generator>`, and removing the `entry` element results in a successful run:
```diff
from typing import Final

import httpx
from httpx import Response
- from pydantic_xml.model import BaseXmlModel
+ from pydantic_xml.model import BaseXmlModel, element
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


# NOTE -- we have to declare the _same_ `nsmap` for our `Entry` class as
# we did in the `Feed` class, otherwise we'll run into the same errors
# from before.
class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP):
    """A blog post entry from the RSS feed."""

    ...


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP):
    """Validate the RSS feed/XML from my blog."""
    
+     # We define `generator` to be a dictionary element to capture its 
+     # attribute keys and values.
+     generator: dict[str, str] = element()
-     entry: Entry


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)  # >>> Feed(generator={'uri': 'https://jekyllrb.com/', 'version': '3.10.0'})

```
But why?
Because of how the `pydantic-xml` model searches for its subfields.
According to the [`pydantic-xml` docs](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/elements.html#elements-search-mode) there are three search methods:
- [Strict (default)](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/elements.html#strict-default)
- [Ordered](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/elements.html#ordered)
- [Unordered](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/elements.html#unordered)

Both the _strict_ and _ordered_ search methods require the model's subfields to mirror the order in the XML document,
but the latter offers a bit more flexibility by allowing "unknown" fields to be skipped.
Or in our case, fields we don't care about.
That means
setting `search_mode="ordered"` in our `Feed` signature should allow us to skip all the way to our `Entry` subfield.
```diff
from typing import Final

import httpx
from httpx import Response
+ from pydantic_xml.model import BaseXmlModel
- from pydantic_xml.model import BaseXmlModel, element
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


# NOTE -- we have to declare the _same_ `nsmap` for our `Entry` class as
# we did in the `Feed` class, otherwise we'll run into the same errors
# from before.
class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP):
    """A blog post entry from the RSS feed."""

    ...


- class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP):
+ class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
    """Validate the RSS feed/XML from my blog."""

-     # We define `generator` to be a dictionary element to capture its 
-     # attribute keys and values.
-     generator: dict[str, str] = element()
+     entry: Entry


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)  # >>> Feed(entry=Entry())

```
And it does.

The downside to this is we lose everything between the `<feed>` and `<entry>` tags.
In `pydantic`,
we'd be able
to see everything else in the
[`model_extra`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_extra)
if we set the [`model_config`](https://docs.pydantic.dev/latest/concepts/config/) to allow for it.
Unfortunately, this doesn't work in `pydantic-xml`.

#### Duplicate Field Names
This is the next entry in my XML, minus the content and summary.
```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <generator uri="https://jekyllrb.com/" version="3.10.0">Jekyll</generator>
    <link href="/feed.xml" rel="self" type="application/atom+xml"/>
    <link href="/" rel="alternate" type="text/html"/>
    <updated>2024-12-13T02:39:38+00:00</updated>
    <id>/feed.xml</id>
    <title type="html">My Blog</title>
    <subtitle>Where I write things...</subtitle>
    <author>
        <name>Ian Thompson</name>
    </author>
    <entry>
        <title type="html">isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit</title>
        <link href="/2024/12/12/isort.html" rel="alternate" type="text/html"
              title="isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit"/>
        <published>2024-12-12T00:00:00+00:00</published>
        <updated>2024-12-12T00:00:00+00:00</updated>
        <id>/2024/12/12/isort</id>
        <content type="html" xml:base="/2024/12/12/isort.html">...</content>
        <author>
            <name>Ian Thompson</name>
        </author>
        <summary type="html">...</summary>
    </entry>
    <entry>
        <title type="html">PyCharm: Projects &amp;amp; Environments</title>
        <link href="/2024/12/03/pycharm-projects-envs.html" rel="alternate" type="text/html"
              title="PyCharm: Projects &amp;amp; Environments"/>
        <published>2024-12-03T00:00:00+00:00</published>
        <updated>2024-12-03T00:00:00+00:00</updated>
        <id>/2024/12/03/pycharm-projects-envs</id>
        <content type="html" xml:base="/2024/12/03/pycharm-projects-envs.html">...</content>
        <author>
            <name>Ian Thompson</name>
        </author>
        <summary type="html">...</summary>
    </entry>
</feed>
```

You'll notice that each `<entry>` tag is at the same level.
In JSON, this would be the equivalent of having multiple fields with the same name:
```json
{
  "Field": "Value1",
  "Field": "Value2"
}
```

And validating this with `pydantic` would yield some interesting results:
```python
from typing import Annotated

from pydantic.fields import Field
from pydantic.main import BaseModel
from rich.console import Console


class Model(BaseModel):
    field: Annotated[str, Field(alias="Field")]
    field: Annotated[str, Field(alias="Field")]


if __name__ == "__main__":
    json_as_python_dict = {
        "Field": "Value1",
        "Field": "Value2",
    }
    model = Model(**json_as_python_dict)
    console = Console()
    console.print(model)  # >>> Model(field="Value2")

```

While having multiple keys with the same name in JSON is technically allowed,
it's not good practice.
And using Python to read the JSON resolves it to a `dict` which _can't_ have duplicate keys.
In fact,
defining a dictionary with duplicate keys is roughly equivalent
to merging two `dict` objects with the same key(s).
This results in a "last seen wins" value-assignment to the duplicate key
(see [PEP 584](https://peps.python.org/pep-0584/) for more details).

What about XML?
Duplicate tag names are allowed; how does `pydantic-xml` handle them?
It turns out that by simply differentiating the attribute names,
e.g. "entry1" and "entry2,"
the `pydantic-xml` model will assign the tags in the order it discovers them.
```python
from datetime import datetime
from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel, element
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP):
    """A blog post entry from the RSS feed."""

    # NOTE -- I'm validating some of the entry subfields to 
    # differentiate from other entries.
    title: str = element()
    published: datetime = element()
    updated: datetime = element()


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

    entry1: Entry
    entry2: Entry


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
```text
Feed(
    entry1=Entry(
        title='isort + git: Cleaner Import Statements for Those Who Don’t Like 
pre-commit',
        published=datetime.datetime(2024, 12, 12, 0, 0, tzinfo=TzInfo(UTC)),
        updated=datetime.datetime(2024, 12, 12, 0, 0, tzinfo=TzInfo(UTC))
    ),
    entry2=Entry(
        title='PyCharm: Projects &amp; Environments',
        published=datetime.datetime(2024, 12, 3, 0, 0, tzinfo=TzInfo(UTC)),
        updated=datetime.datetime(2024, 12, 3, 0, 0, tzinfo=TzInfo(UTC))
    )
)
```

That's kind of convenient,
but what if I don't know how many `<entry>` tags are in the XML?
The `pydantic-xml` model has
that covered with a thing
called [_homogenous collections_](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/homogeneous.html#homogeneous-collections).
```diff
from datetime import datetime
from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel, element
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP):
    """A blog post entry from the RSS feed."""

    # NOTE -- I'm validating some of the entry subfields to 
    # differentiate from other entries.
    title: str = element()
    published: datetime = element()
    updated: datetime = element()


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

-     entry1: Entry
-     entry2: Entry
+     entries: list[Entry]


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
```text
Feed(
    entries=[
        Entry(
            title='isort + git: Cleaner Import Statements for Those Who Don’t 
Like pre-commit',
            published=datetime.datetime(2024, 12, 12, 0, 0, 
tzinfo=TzInfo(UTC)),
            updated=datetime.datetime(2024, 12, 12, 0, 0, tzinfo=TzInfo(UTC))
        ),
        Entry(
            title='PyCharm: Projects &amp; Environments',
            published=datetime.datetime(2024, 12, 3, 0, 0, tzinfo=TzInfo(UTC)),
            updated=datetime.datetime(2024, 12, 3, 0, 0, tzinfo=TzInfo(UTC))
        )
    ]
)
```
This is probably my favorite feature in `pydantic-xml`.

# Bonus Features
As I wrap up my blog's RSS feed class, I'd like to highlight a few features of `pydantic-xml`.
First, you don't have to create a new model `class` for every XML subfield.
For example, here is how I'd validate the `<author>` tag _with_ a model:
```python
from datetime import datetime
from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel, element
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


class Author(BaseXmlModel, tag="author", nsmap=NSMAP):
    """A blog post author from the RSS feed."""

    name: str = element(tag="name")


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    """A blog post entry from the RSS feed."""

    title: str = element()
    published: datetime = element()
    updated: datetime = element()
    author: Author


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

    entries: list[Entry] = element()


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
And here is how I'd do it _without_ an `Author` model:
```diff
from datetime import datetime
from typing import Final

import httpx
from httpx import Response
- from pydantic_xml.model import BaseXmlModel, element
+ from pydantic_xml.model import BaseXmlModel, element, wrapped
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


- class Author(BaseXmlModel, tag="author", nsmap=NSMAP):
-     """A blog post author from the RSS feed."""
- 
-     name: str = element(tag="name")


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    """A blog post entry from the RSS feed."""

    title: str = element()
    published: datetime = element()
    updated: datetime = element()
-     author: Author
+   author: str = wrapped(path="author", entity=element(tag="name"))


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

    entries: list[Entry] = element()


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
This second approach uses the [`wrapped`](https://pydantic-xml.readthedocs.io/en/stable/pages/data-binding/wrapper.html#wrapper) function.
When a field doesn't have a lot of important attributes that I'd like to validate, e.g. the `<author>` tag,
I'd use `wrapped` instead of defining a new model class.
> [!NOTE]
> 
> This changes the type of `Feed.entry.author`:
> ```diff
> Feed(
>     entries=[
>         Entry(
>             ...,
> -             author=Author(name='Ian Thompson')
> +             author='Ian Thompson'
>         )
>     ]
> )
> ```

A more direct/less verbose way of using `wrapped` would be to only supply an argument to the `path` parameter:
```diff
from datetime import datetime
from typing import Final

import httpx
from httpx import Response
from pydantic_xml.model import BaseXmlModel, element, wrapped
from rich.console import Console

NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}


class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    """A blog post entry from the RSS feed."""

    title: str = element()
    published: datetime = element()
    updated: datetime = element()
-     author: str = wrapped(path="author", entity=element(tag="name"))
+     author: str = wrapped(path="author/name")


class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):

    """Validate the RSS feed/XML from my blog."""

    entries: list[Entry] = element()


if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml: bytes = resp.content
    console = Console()
    model = Feed.from_xml(source=xml)
    console.print(model)

```
I see the `entity` parameter as more useful when accessing tag _attributes_,
rather than tags themselves.