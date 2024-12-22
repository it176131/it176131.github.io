---
layout: "post"
title: "pydantic-xml: Parsing My XML Feed"
date: 2024-12-22
---

I thought
it'd be cool
to add my most recent blog post to my [GitHub profile](https://github.com/it176131)
using a custom GitHub action and workflow.
To do that, I'd need to know which post was most recently published along with its title, URL, etc.
After looking at the [GoodReads workflow](https://github.com/it176131/it176131/blob/dev/.github/workflows/goodreads-books-workflow.yml) on my profile,
I figured I could get that information from my blog's RSS feed.

> [RSS](https://en.wikipedia.org/wiki/RSS) is a web feed that allows users and applications to access udpates to websites in a standardized,
> computer-readable format.
> 
> —Wikipedia

Accessing my blog's RSS feed is as simple as adding _/feed.xml_ to the end of its URL.
Check it out here 👉 [https://it176131.github.io/feed.xml](https://it176131.github.io/feed.xml).