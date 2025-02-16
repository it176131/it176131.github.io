---
layout: "post"
title: "Includes & Layouts: Making My Site a Bit More Automated"
date: 2025-02-16
---

I think this post will be short.
It will start with a recap of my [_2024:
Year in Review_]({{ site.baseurl }}{% link _posts/2025-01-31-year-in-review.md %})
post where I mentioned wanting to write better posts and track web traffic.
From there I'll introduce that I'm using [Google Analytics](https://developers.google.com/analytics).

To use Google Analytics I need to add an HTML `<script>` element to all of my posts just below the `<head>` tag.
This raised a problem—a large number of my posts are written in [Markdown](https://en.wikipedia.org/wiki/Markdown),
which means I don't have a direct ability to add/modify the HTML with the Google Analytics `<script>`.

I knew
that [Jekyll](https://jekyllrb.com/) performed a conversion of my Markdown to HTML before being deployed/published.
This lead me to search for the "template" used by Jekyll for my posts, and later, for all pages on my site.

With some digging I discovered the `_includes/` and `_layouts/` directories.
The `_layouts/` directory houses the "templates" used by Jekyll to convert my pages to HTML.
The `_includes/` directory holds snippets of HTML that don't do anything by themselves,
but can augment the HTML in a layout template if "included."

This is where [front matter](https://jekyllrb.com/docs/front-matter/) at the top of each post started to make sense.
On any given post on my blog you'll find a section at the top called _front matter_.
Its job is to tell Jekyll _how to format this Markdown when converting to HTML_.
> [!NOTE]
> 
> Verify this!!

It's represented as a block of yaml-like text enclosed by three dashes on top and bottom.
For example:
```yaml
---
front matter goes here!
---
```