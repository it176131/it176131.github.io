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

# `pydantic-xml`
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
Viewing my blog's RSS feed was straightforward; parsing and validating it wasn't (at first).

I learned there are some distinct differences between JSON and XML:
- Field names, i.e. "keys", at the same level _must be unique_ in JSON
- Elements, i.e. "tags", at the same level _don't have to be unique_ in XML
- Fields are ordered in JSON, but can be parsed and validated by `pydantic` in _any_ order
- Elements are ordered in XML, and have to be parsed and validated in their _given_ order by `pydantic-xml` (by default)