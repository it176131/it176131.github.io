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