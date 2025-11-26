---
layout: "post"
title: "Actions & Workflows: Automatically Updating My GitHub Profile with Recent Blog Posts"
date: 2025-01-25
images: "/assets/images/2025-01-25-recent-posts-action"
---
<head>
   <style>

      h1 {
          font-size: 2.5em; /* Adjust to desired size */
      }
      
      h2 {
          font-size: 1.5em; /* Adjust to desired size */
      }
      
      h3 {
          font-size: 1.2em; /* Adjust to desired size */
      }

   </style>
</head>

First post of 2025!

I ended 2024 with my post, [_pydantic-xml: Parsing My RSS Feed_]({{ site.baseurl }}{% link _posts/2024/12/2024-12-23-pydantic-xml.md %}),
and mentioned that I was trying to add my most recent blog post to my GitHub profile using a custom GitHub action and workflow.
I'm happy to share that after a couple of weeks, I figured it out. 😎

I won't bore you with every struggle I experienced.
Instead, I'll share what files I had to create,
how they interact with each other from a high level,
and then give a (mostly) line-by-line breakdown of the important stuff.

# The files
All together, I created four new files and modified two others:

|          | File                                                             |
|----------|------------------------------------------------------------------|
| New      | action.yml<br>Dockerfile<br>recent-posts.yml<br>requirements.txt |
| Modified | main.py<br>README.md                                             |

The files are across two repos,
my [blog repo](https://github.com/it176131/it176131.github.io) and my [profile repo](https://github.com/it176131/it176131).
This organizes things and allows me
to keep the [_action_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#actions) in the blog repo,
and the [_workflow_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#workflows) in the profile repo.

Here is the layout of my two repos.
```
📂 it176131.github.io  # blog repo
└── 📂 .github
    └── 📂 actions
        └── 📂 recent-posts
            ├── 🔧 action.yml  # The action metadata file
            ├── 🐋 Dockerfile  # Instructions to build the Docker container
            ├── 🐍 main.py  # Python script to update the input (README.md)
            └── 📄 requirements.txt  # Python package dependencies for main.py

📂 it176131  # profile repo
├── 📂 .github
│   └── 📂 workflows
│       └── 🔧 recent-posts.yml  # The workflow file
└── 📓 README.md  # My "profile"
```

# The interactions
There are six interactions among the files that result in the `README.md` being updated.
Because the files have unique names, I will reference them as if they were local to each other.
For example, I will reference `it176131/.github/workflows/recent-posts.yml` as `recent-posts.yml`.
> For your convenience, each file name will have a [tooltip ℹ️](## "Hover over the filenames") with the full path so you can keep them straight 😉.

1. [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") checks out the repository, giving it access to [_README.md_ ℹ️](## "it176131/README.md").
2. [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") calls [_action.yml_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/action.yml") with inputs `readme` (default [_README.md_ ℹ️](## "it176131/README.md")) and `num-entries` (default `5`).
3. [_action.yml_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/action.yml") informs GitHub
   to build a Docker container using the [_Dockerfile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile").
4. The Docker container produced by [_Dockerfile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile") installs the packages in [_requirements.txt_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/requirements.txt") and runs [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py") with the inputs from *step 1*.
5. [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py") takes the inputs and updates the [_README.md_ ℹ️](## "it176131/README.md") with the latest posts.
6. [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") checks if [_README.md_ ℹ️](## "it176131/README.md") has been modified, commiting and pushing any changes.

That's quite a bit of interaction.
Let's open up the files and see what's going on under the hood.

# The breakdown
I'll start with [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml")
as it's the first file referenced in _step 1_.

## _recent-posts.yml_
### Some meta-information
The [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") is a _workflow_ file.
It has an optional
[`name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#name) to help
identify it in the GitHub UI.

```yaml
name: "Update README with most recent blog post"
```

|------------------------------------------------|---------------------------------------------|
| ![Workflow Name in GitHub UI 1]({{ page.images | relative_url }}/gh_action_workflow_ui1.png) |![Workflow Name in GitHub UI 2]({{ page.images | relative_url }}/gh_action_workflow_ui2.png)|

Workflow files run when triggered by an event.
Those "events"
are defined via the required [`on`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#on) keyword.
```yaml
on:
```

This particular workflow has two types of triggering events:
- a [`schedule`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onschedule) that runs every five minutes (though I'll probably change that),

```yaml
   schedule:
    - cron: "* * * * *"
```

- and a [`push`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push) to either the "main" or "master" [`branches`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#running-your-workflow-only-when-a-push-to-specific-branches-occurs)

```yaml
  push:
    branches: ["main", "master"]
```

They are combined under the same `on`:
```yaml
on:
  push:
    branches: ["main", "master"]

  schedule:
     - cron: "* * * * *"
```

When a workflow is triggered, it has to do one or more things.
Those things are called [`jobs`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobs).
This workflow has one job with the [`<job_id>`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_id),
`recent_post_job`.
It has the more human-readable [`name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idname), "Recent Post," which is what we see in the GitHub UI,

|-------------------------------------------|---------------------------------|
| ![Job Name in GitHub UI 1]({{ page.images | relative_url }}/gh_job_ui1.png) | ![Job Name in GitHub UI 2]({{ page.images | relative_url }}/gh_job_ui2.png)|

and it [`runs-on`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idruns-on) the [latest version of Ubuntu](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for-public-repositories).
```yaml
jobs:
  recent_post_job:
    runs-on: ubuntu-latest
    name: Recent Post
```

Now for the moment we've all been waiting for...
### Step 1
> [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") checks out the repository, giving it access to [_README.md_ ℹ️](## "it176131/README.md").

Each [`step`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps) under our `recent_post_job` has a [`name`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsname),
and _step 1_'s name is "Checkout repo."

To add, delete, modify, and even read a file in the repository requires it to be checked out.
_Step 1_ [`uses`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses) the GitHub action
[`actions/checkout@v4`](https://github.com/actions/checkout?tab=readme-ov-file#checkout-v4) to do this.
I won't get to in the weeds here,
but if you don't do this step, you won't be able to do anything with the _README.md_.
```yaml
jobs:
  recent_post_job:
    runs-on: ubuntu-latest
    name: Recent Post
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
```

### Step 2
> [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") calls [_action.yml_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/action.yml") with inputs `readme` (default [_README.md_ ℹ️](## "it176131/README.md")) and `num-entries` (default `5`).

This is where we leave my _profile_ repo for my _blog_ repo.

The "Recent post action"
step `uses` the action, `it176131/it176131.github.io/.github/actions/recent-posts@main`,
from my blog repo [`with`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepswith) the inputs:
- `readme: "./README.md"`
- `num-entries: 5`

> [!NOTE]
> 
> Order is important here for a reason you'll see in _step 5_.

```yaml
jobs:
  recent_post_job:
#     ...
    steps:
#      ...

      - name: Recent post action
        uses: "it176131/it176131.github.io/.github/actions/recent-posts@main"
        with:
          readme: "./README.md"
          num-entries: 5
```

## _action.yml_
### Some (more) meta-information
Calling an action requires an _action.yml_ file.
It contains both general information about the action and instructions for GitHub to run it.

This particular action's [`name`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#name) is "Recent Posts".
It has the [`description`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#description), "Get the most recent blog post metadata,"
and an optional [`author`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#author), yours truly.

```yaml
name: "Recent Posts"
author: "Ian Thompson"
description: "Get the most recent blog post metadata."
```

It defines the expected [`inputs`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputs) with an [`<input_id>`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_id),
and provides a [`description`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddescription),
[`default`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddefault) value,
and whether it's [`required`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#inputsinput_idrequired).

```yaml
inputs:
  readme:
    description: "Path to the README.md"
    required: false
    default: "./README.md"

  num-entries:
    description: "Number of blog entries to show"
    required: false
    default: 5
```

> [!NOTE]
> 
> I declared both of my `inputs` as optional, i.e. `required: false`.
> If I removed the `default` values I'd have to change them to `required: true`.
 
### Step 3
> [_action.yml_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/action.yml") informs GitHub to build a Docker container using the [_Dockerfile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile").

This last part of the _action.yml_ tells GitHub
what kind of action it [`runs`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runs).
We're [`using`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsusing-for-docker-container-actions) Docker
and the instructions
to build the container are in our [_DockerFile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile") [`image`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsimage).
As the container is starting,
GitHub passes the [`args`](https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#runsargs) from our [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml"),
or the defaults if we hadn't passed any.

{% raw %}
```yaml
runs:
  using: "docker"
  image: "Dockerfile"
  args:
    - ${{ inputs.readme }}
    - ${{ inputs.num-entries }}
```
{% endraw %}

## _Dockerfile_
### Step 4
> The Docker container produced by [_Dockerfile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile")
> installs the packages in [_requirements.txt_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/requirements.txt")
> and runs [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py")
> with the inputs from *step 1*.

The Docker container
produced via the [_DockerFile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile") comes [`FROM`](https://docs.docker.com/reference/dockerfile/#from) a Python 3.13 base image.

```dockerfile
FROM python:3.13
```

It then makes a [`COPY`](https://docs.docker.com/reference/dockerfile/#copy) of the [_requirements.txt_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/requirements.txt") file to its primary directory.

```dockerfile
COPY requirements.txt ./
```

From here it will [`RUN`](https://docs.docker.com/reference/dockerfile/#run) the `pip install` command on the newly copied _requirements.txt_,
satisfying the dependencies of [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py").

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt \
```

After that,
it will copy the rest of the files in the same directory as [_DockerFile_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/Dockerfile") to the container directory,
before running [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py") as an [`ENTRYPOINT`](https://docs.docker.com/reference/dockerfile/#entrypoint).

```dockerfile
COPY . ./

ENTRYPOINT ["python", "/main.py"]
```

> [!NOTE]
> 
> Running the Python script as an entrypoint is required if you want
> [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py")
> to receive the `args` from [_action.yml_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/action.yml")
> and [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml").

## _main.py_

I'm not going
to walk through the [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py") file line-by-line
as I covered most of it in my [previous post]({{ site.baseurl }}{% link _posts/2024/12/2024-12-23-pydantic-xml.md %}).
However,
I will note that I made some changes so that it can directly modify the [_README.md_ ℹ️](## "it176131/README.md")
file.
I will walk through what I consider the most important parts.

Some changes required me to update my import statements.
```diff
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

```

I also decided that I wanted more than the single most recent blog post,
so I changed `Feed.entry` to `Feed.entries`.
```diff
 class Feed(BaseXmlModel, tag="feed", nsmap=NSMAP, search_mode="ordered"):
     """Validate the RSS feed/XML from my blog."""

-    # We limit to the first <entry> from the RSS feed as it is the most
-    # recently published.
-    entry: Entry
+    # We collect all <entry> tags from the RSS feed.
+    entries: list[Entry]

```

### Step 5
> [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py")
> takes the inputs and updates the [_README.md_ ℹ️](## "it176131/README.md")
> with the latest posts.

To accept the inputs,
I needed to modify my script's signature with both a `readme` and `num_entries` parameter.
```diff
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
```

The `num_entries` argument allowed me to dynamically control how many
blog posts to get from my `Feed.entries` list.
```diff
     resp: Response = httpx.get(url=f"{BLOG_URL}/feed.xml")
     xml: bytes = resp.content
-    console = Console()
     model = Feed.from_xml(source=xml)
-    console.print(model.model_dump_json(indent=2))
+    entries = model.entries[:num_entries]
+
```

Modifying the [_README.md_ ℹ️](## "it176131/README.md") was a bit more involved.
First I had to read the file in.
Then, with the help of a regular expression,
I could find the text between two HTML comments and replace it with my entries.
After that I could overwrite the [_README.md_ ℹ️](## "it176131/README.md") and my work would be done.
```diff
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

### _README.md_
Using a regular expression only works if the HTML comments already exist, which they didn't at first.
This meant that I had to modify the [_README.md_ ℹ️](## "it176131/README.md")
_before_ my workflow could do anything.

In a previous version of my [_README.md_ ℹ️](## "it176131/README.md") I had a section called "Articles"
that originally held links to my [Medium content](https://medium.com/@ianiat11).
I don't really write on [Medium](https://medium.com/) anymore,
and figured this would be a good place to put the output of my workflow.

```diff
 # Articles ✍
-![Medium](https://github-read-medium-git-main.pahlevikun.vercel.app/latest?username=ianiat11&limit=6&theme=dracula)
+<!-- BLOG START -->
+<!-- BLOG END -->
```

Now my script has a place between two comments to write my blog entries 😎.

## _recent-posts.yml_ (revisited)
### Step 6
> [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") checks if [_README.md_ ℹ️](## "it176131/README.md") has been modified, commiting and pushing any changes.

After [_main.py_ ℹ️](## "it176131.github.io/.github/actions/recent-posts/main.py") has finished,
the action is complete,
and we return to [_recent-posts.yml_ ℹ️](## "it176131/.github/workflows/recent-posts.yml") with the
(possibly) modified [_README.md_ ℹ️](## "it176131/README.md").

The final step in the workflow is called "Commit README,"
and that's pretty much what it will [`run`](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsrun).
First, `git`
configures the `user.email` and `user.name` so I can tell when the action is performing a commit versus myself.
Next, it determines if the [_README.md_ ℹ️](## "it176131/README.md") has actually been modified.
If it has, it will add, commit, and push the changes.
Otherwise, the step ends along with the workflow.

```yaml
jobs:
  recent_post_job:
    runs-on: ubuntu-latest
    name: Recent Post
    steps:
#      ...

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

# Conclusion
And that's it!
On the first run of this workflow there were obviously some changes to my [_README.md_ ℹ️](## "it176131/README.md"):

```diff
# Articles ✍
<!-- BLOG START -->
+- [pydantic-xml: Parsing My RSS Feed](https://it176131.github.io/2024/12/23/pydantic-xml.html) by Ian Thompson
+- [isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit](https://it176131.github.io/2024/12/12/isort.html) by Ian Thompson
+- [PyCharm: Projects &amp; Environments](https://it176131.github.io/2024/12/03/pycharm-projects-envs.html) by Ian Thompson
+- [Dynamic Enums](https://it176131.github.io/2024/11/29/dynamic-enums.html) by Ian Thompson
+- [SpaCy: Extensions](https://it176131.github.io/2024/11/27/spacy-extensions.html) by Ian Thompson
<!-- BLOG END -->
```

I went a bit further and also updated the section title
and moved my blog link from the top of my profile to the new section title.

```diff
 ### Hi there 👋 I'm Ian 🙂
-Checkout my blog! 👉 https://it176131.github.io/

 # Reputation ✔
 <a href="https://stackoverflow.com/users/6509519/ian-thompson"><img src="https://stackoverflow.com/users/flair/6509519.png?theme=dark" width="208" height="58" alt="profile for Ian
 Thompson at Stack Overflow, Q&amp;A for professional and enthusiast programmers" title="profile for Ian Thompson at Stack Overflow, Q&amp;A for professional and enthusiast programmers"></a>

-# Articles ✍
+# Recent Articles From My [Blog](https://it176131.github.io/) ✍
 <!-- BLOG START -->
 - [pydantic-xml: Parsing My RSS Feed](https://it176131.github.io/2024/12/23/pydantic-xml.html) by Ian Thompson
 - [isort + git: Cleaner Import Statements for Those Who Don’t Like pre-commit](https://it176131.github.io/2024/12/12/isort.html) by Ian Thompson
```

And after this entry is published, there will be an additional change.

I hope this has been informative and provides enough details on GitHub actions and workflows for you to create your own.
Happy coding 🤓.