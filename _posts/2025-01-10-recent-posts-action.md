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
> When I first wrote my Dockerfile I used `CMD` instead of `ENTRYPOINT`
> because that's what the example looked like on the 
> [Docker website](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/).
> This led to an issue when trying to submit arguments to my Python script via the workflow.

___
# Footnotes
[^1]: [_Creating your first workflow_](https://docs.github.com/en/actions/writing-workflows/quickstart#creating-your-first-workflow)
[^2]: [_Creating a Docker container action_](https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-docker-container-action)