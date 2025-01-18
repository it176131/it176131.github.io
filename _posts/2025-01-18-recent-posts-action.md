---
layout: "post"
title: "Actions & Workflows: Automatically Updating My GitHub Profile with Recent Blog Posts"
date: 2025-01-10
---

First post of 2025!

I ended 2024 with my post, [_pydantic-xml:
Parsing My RSS Feed_]({{ site.baseurl }}{% link _posts/2024-12-23-pydantic-xml.md %}),
and mentioned that I was trying to add my most recent blog post to my GitHub profile using a custom GitHub action and workflow.
I'm happy to share that after a couple of weeks, I figured it out. 😎

# Action
Writing a GitHub action wasn't as straightforward as I thought it would be.
I checked out some tutorials from the [GitHub Actions documentation](https://docs.github.com/en/actions)[^1] [^2]
and decided that because I don't know JavaScript, I'd use a Docker container to execute my Python script.

To use a Docker container, I need a Dockerfile.
Here's what mine looks like:
```dockerfile
FROM python:3.13

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENTRYPOINT ["python", "/main.py"]
```

This file provides instructions to the GitHub action on how to build a container with Python 3.13,
install my script's dependencies via the requirements.txt file, then declare `python /main.py` as an _entrypoint_.
> [!NOTE]
> 
> When I first wrote my Dockerfile I used [`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) instead of [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint)
> because that's what the example looked like on the 
> [Docker website](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/).
> This led to an issue when trying to submit arguments to my Python script via the workflow.
> 
> It's also worth noting that the Dockerfile used in the GitHub tutorial does use `ENTRYPOINT`, but not a Python script which confused me.

After I wrote the Dockerfile I worked on my action.yml file:
```yaml
name: "Recent Posts"
author: "Ian Thompson"
description: "Get the most recent blog post metadata."
inputs:
  readme:
    description: "Path to the README.md"
    required: false
    default: "./README.md"

  num-entries:
    description: "Number of blog entries to show"
    required: false
    default: 5

runs:
  using: "docker"
  image: "Dockerfile"
  args:
    - ${{ inputs.readme }}
    - ${{ inputs.num-entries }}
```

If you'll recall, my original Python script didn't take any arguments or return an output.
It only printed the most recent blog entry as a JSON string.
```python
# My original main.py contents.

from datetime import datetime
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
    console.print(model.model_dump_json(indent=2))

```
```json
{
  "entry": {
    "title": "pydantic-xml: Parsing My RSS Feed",
    "relative_url": "/2024/12/23/pydantic-xml.html",
    "published": "2024-12-23T00:00:00Z",
    "updated": "2024-12-23T00:00:00Z",
    "author": "Ian Thompson",
    "link": "https://it176131.github.io/2024/12/23/pydantic-xml.html"
  }
}
```

I decided that I'd like to show more than one blog post (similar to my Goodreads shelves) on my README.md, but wasn't sure how many.
I updated my script to accept an argument allowing me to try several options.

To actually update my README.md, I'd need to open it from within the script,
add my blog post, save it, then git add, commit and push the changes.
Here are my changes.
```diff
-# My original main.py contents.
+# My current main.py contents.

 from datetime import datetime
-from typing import Final
+import re
+from typing import Annotated, Final

 import httpx
 from httpx import Response
 from pydantic.networks import HttpUrl
+from pydantic.types import FilePath
 from pydantic_xml.model import (
     attr, BaseXmlModel, computed_element, element, wrapped
 )
-from rich.console import Console
+from typer import Typer
+from typer.params import Argument

 BLOG_URL = "https://it176131.github.io"
 NSMAP: Final[dict[str, str]] = {"": "http://www.w3.org/2005/Atom"}
+app = Typer()


 class Entry(BaseXmlModel, tag="entry", nsmap=NSMAP, search_mode="ordered"):
    ...

 class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
     """Validate the RSS feed/XML from my blog."""

-    # We limit to the first <entry> from the RSS feed as it is the most
-    # recently published.
-    entry: Entry
+    # We collect all <entry> tags from the RSS feed.
+    entries: list[Entry]


-if __name__ == "__main__":
+@app.command()
+def main(
+        readme: Annotated[
+            FilePath,
+            Argument(help="Path to file where metadata will be written.")
+        ],
+        num_entries: Annotated[
+            int,
+            Argument(help="Number of blog entries to write to the `readme`.")
+        ],
+) -> None:
+    """Write most recent blog post metadata to ``readme``."""
     resp: Response = httpx.get(url=f"{BLOG_URL}/feed.xml")
     xml: bytes = resp.content
-    console = Console()
     model = Feed.from_xml(source=xml)
-    console.print(model.model_dump_json(indent=2))
+    entries = model.entries[:num_entries]
+
+    with readme.open(mode="r") as f:
+        text = f.read()
+
+    pattern = r"(?<=<!-- BLOG START -->)[\S\s]*(?=<!-- BLOG END -->)"
+    template = "- [{title}]({link}) by {author}"
+    repl = "\n".join(
+        [
+            template.format(title=e.title, link=e.link, author=e.author)
+            for e in entries
+        ]
+    )
+    new_text = re.sub(pattern=pattern, repl=f"\n{repl}\n", string=text)
+    with readme.open(mode="w") as f:
+        f.write(new_text)
+
+
+if __name__ == "__main__":
+    app()

```


___
# Footnotes
[^1]: [_Creating your first workflow_](https://docs.github.com/en/actions/writing-workflows/quickstart#creating-your-first-workflow)
[^2]: [_Creating a Docker container action_](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-docker-container-action)