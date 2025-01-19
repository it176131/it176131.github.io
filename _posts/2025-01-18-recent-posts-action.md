---
layout: "post"
title: "Actions & Workflows: Automatically Updating My GitHub Profile with Recent Blog Posts"
date: 2025-01-18
---

First post of 2025!

I ended 2024 with my post, [_pydantic-xml: Parsing My RSS Feed_]({{ site.baseurl }}{% link _posts/2024-12-23-pydantic-xml.md %}),
and mentioned that I was trying to add my most recent blog post to my GitHub profile using a custom GitHub action and workflow.
I'm happy to share that after a couple of weeks, I figured it out. 😎

I won't bore you with every struggle I experienced.
Instead, I'll share what files I had to create,
how they interact with each other from a high level,
and then give a (mostly) line-by-line breakdown of the important stuff.

# The files
To keep things organized,
I decided
to put the [_action_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#actions) in the [blog repo](https://github.com/it176131/it176131.github.io),
and the [_workflow_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#workflows) in the [profile repo](https://github.com/it176131/it176131).
```
📂 it176131.github.io
└── 📂 .github
    └── 📂 actions
        └── 📂 recent-posts
            ├── 🔧 action.yml  # The action metadata file
            ├── 🐋 Dockerfile  # Instructions to build the Docker container
            ├── 🐍 main.py  # Python script to pull/parse the XML and update the input (README.md)
            └── 📄 requirements.txt  # Python package dependencies for main.py

📂 it176131
├── 📂 .github
│   └── 📂 workflows
│       └── 🔧 recent-posts.yml  # The workflow file
└── 📓 README.md  # My "profile"
```

There are three [types of actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#types-of-actions):
[Docker container](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#docker-container-actions), [JavaScript](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#javascript-actions), and [composite actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#composite-actions).
I opted to use a [Docker container](https://www.docker.com/resources/what-container/) because:
1. I don't know enough [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
to be comfortable writing an action from scratch, and
2. This is my first custom action and workflow, so I don't think I need to create a _composite action_ just yet.

Using a Docker container also allows me
to use my preexisting Python script from the last [post]({{ site.baseurl }}{% link _posts/2024-12-23-pydantic-xml.md %}).

# Step 1:
`it176131/.github/workflows/recent-posts.yml` calls `it176131.github.io/.github/actions/recent-posts/action.yml` and sends argument inputs.

```yaml
name: "Update README with most recent blog post"
on:
  push:
    branches: ["main", "master"]

  schedule:
    - cron: "* * * * *"

permissions:
  contents: write

jobs:
  recent_post_job:
    runs-on: ubuntu-latest
    name: Recent Post
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Recent post action
        uses: "it176131/it176131.github.io/.github/actions/recent-posts@recent-posts"
        with:
          readme: "./README.md"
          num-entries: 5

      - name: Commit README
        run: |
          git config user.email github-actions@github.com
          git config user.name github-actions
          has_diff=$(git diff main --name-only -- README.md)
          if [ $has_diff ]; then
            git add README.md
            git commit -m "Synced and updated with most recent it176131.github.io blog post"
            git push
          fi
```

YAML Keywords in `recent-posts.yml` Workflow:
- [`name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#name)
- [`on`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#on)
- [`on.push`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push)
- [`on.push.branches`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#running-your-workflow-only-when-a-push-to-specific-branches-occurs)
- [`on.schedule`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onschedule)
- [`on.schedule.cron`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule)
- [`permissions`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#permissions)
- `permissions.contents` ???
- [`jobs`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobs)
- [`jobs.recent_post_job`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_id)
- [`jobs.recent_post_job.runs-on`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idruns-on)
- [`jobs.recent_post_job.name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idname)
- [`jobs.recent_post_job.steps`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps)
- [`jobs.recent_post_job.steps.name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsname)
- [`jobs.recent_post_job.steps.uses`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses)
- [`jobs.recent_post_job.steps.with`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepswith)
- [`jobs.recent_post_job.steps.run`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun)

# The README.md
```markdown
# Recent Articles From My [Blog](https://it176131.github.io/) ✍
<!-- BLOG START -->
<!-- BLOG END -->
```

# Step 2:
`it176131.github.io/.github/actions/recent-posts/action.yml` spins up a Docker 
container using `it176131.github.io/.github/actions/recent-posts/Dockerfile` 
and supplies the argument inputs from `it176131/.github/workflows/recent-posts.yml`.

{% raw %}
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
{% endraw %}

YAML Keywords in `action.yml` Action:
- [`name`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#name)
- [`author`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#author)
- [`description`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#description)
- [`inputs`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputs)
- [`inputs.readme`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_id)
- [`inputs.readme.description`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddescription)
- [`inputs.readme.required`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_idrequired)
- [`inputs.readme.default`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddefault)
- [`runs`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runs)
- [`runs.using`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsusing-for-docker-container-actions)
- [`runs.image`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsimage)
- [`runs.args`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsargs)

# Step 3:
The Docker container produced by `it176131.github.io/.github/actions/recent-posts/Dockerfile`:
- Installs Python 3.13
- Copies `it176131.github.io/.github/actions/recent-posts/requirements.txt` to its container directory and installs its contents
- Copies the remaining files in `it176131.github.io/.github/actions/recent-posts/` to its container directory
- Declares the `ENTRYPOINT` `python /main.py` and submits the argument inputs to the `main.py` script

```dockerfile
FROM python:3.13

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENTRYPOINT ["python", "/main.py"]
```

Docker Instructions in `Dockerfile`:
- [`FROM`](https://docs.docker.com/reference/dockerfile/#from)
- [`COPY`](https://docs.docker.com/reference/dockerfile/#copy)
- [`RUN`](https://docs.docker.com/reference/dockerfile/#run)
- [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint)

```text
httpx
pydantic-xml
typer
```

# Step 4
`it176131.github.io/.github/actions/recent-posts/main.py` takes the argument inputs and executes.

```python
from datetime import datetime
import re
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

    # We collect all <entry> tags from the RSS feed.
    entries: list[Entry]


@app.command()
def main(
        readme: Annotated[
            FilePath,
            Argument(help="Path to file where metadata will be written.")
        ],
        num_entries: Annotated[
            int,
            Argument(help="Number of blog entries to write to the `readme`.")
        ],
) -> None:
    """Write most recent blog post metadata to ``readme``."""
    resp: Response = httpx.get(url=f"{BLOG_URL}/feed.xml")
    xml: bytes = resp.content
    model = Feed.from_xml(source=xml)
    entries = model.entries[:num_entries]

    with readme.open(mode="r") as f:
        text = f.read()

    pattern = r"(?<=<!-- BLOG START -->)[\S\s]*(?=<!-- BLOG END -->)"
    template = "- [{title}]({link}) by {author}"
    repl = "\n".join(
        [
            template.format(title=e.title, link=e.link, author=e.author)
            for e in entries
        ]
    )
    new_text = re.sub(pattern=pattern, repl=f"\n{repl}\n", string=text)
    with readme.open(mode="w") as f:
        f.write(new_text)


if __name__ == "__main__":
    app()

```

# Step 5
If `it176131.github.io/.github/actions/recent-posts/main.py` completes successfully,
`it176131/.github/workflows/recent-posts.yml` runs the "Commit README" step.
This involves `git` configuring the user to be "github-actions",
checking if the README.md has been modified, and if it has then add, commit, and push.
If it hasn't, end the step.

```diff
# Recent Articles From My [Blog](https://it176131.github.io/) ✍
<!-- BLOG START -->
+- [pydantic-xml: Parsing My RSS Feed](https://it176131.github.io/2024/12/23/pydantic-xml.html) by Ian Thompson
+- [isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit](https://it176131.github.io/2024/12/12/isort.html) by Ian Thompson
+- [PyCharm: Projects &amp; Environments](https://it176131.github.io/2024/12/03/pycharm-projects-envs.html) by Ian Thompson
+- [Dynamic Enums](https://it176131.github.io/2024/11/29/dynamic-enums.html) by Ian Thompson
+- [SpaCy: Extensions](https://it176131.github.io/2024/11/27/spacy-extensions.html) by Ian Thompson
<!-- BLOG END -->
```
