---
layout: "post"
title: "Includes & Layouts: Making My Site a Bit More Automated"
date: 2025-02-16
---

In [_2024:
Year in Review_]({{ site.baseurl }}{% link _posts/2025-01-31-year-in-review.md %})
I mentioned wanting to write better posts and that I would be looking at analytics.
The day after I published,
I figured out how to track web traffic with [Google Analytics](https://developers.google.com/analytics).
I'd like to share the path I took as it taught me more about how my site works under the hood,
as well as give insight to my motivations.

[//]: # (I think this post will be short.)
[//]: # (It will start with a recap of my [_2024:)
[//]: # (Year in Review_]&#40;{{ site.baseurl }}{% link _posts/2025-01-31-year-in-review.md %}&#41;)
[//]: # (post where I mentioned wanting to write better posts and track web traffic.)
[//]: # (From there I'll introduce that I'm using [Google Analytics]&#40;https://developers.google.com/analytics&#41;.)

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

All of my posts have the following front matter keys at a minimum:
- `layout`
- `title`
- `date`

> [!NOTE]
> 
> add Jekyll(?) definitions for each!

I've (almost) always set the layout to "post"
because that's what the [GitHub Pages tutorial](https://github.com/skills/github-pages)
(course?) said to do.
I think the only time I didn't was for my [résumé](https://raw.githubusercontent.com/it176131/it176131.github.io/refs/heads/main/resume.md) when I set the layout to "page".

After finding a file called _post.html_ in the `_layouts/` directory
and seeing a very similar HTML structure to my already-published posts,
I gathered that this was the template Jekyll was using to format my posts
(or at least any page that the layout set to "post" in the front matter).

> [!NOTE]
> 
> I'll want to show the contents of _post.html_ at some point.
> I'd probably also want
> to compare it with my [_Hello World_]({{ site.baseurl }}{% link _posts/2023-12-04-hello-world.md %})
> post (as HTML) so I can draw parallels.

The _page.html_ has references to files in the `_includes/` directory with includes tags.
This would be how I could automatically add the Google Analytics `<script>` element to every page on my site.
But of course, to include it on every page meant using the top-most HTML file rather than the _post.html_ because...
> [!NOTE]
> 
> I don't like how this is written/how it sounds.

After creating an `analytics.html` file in my own repo's `_includes/` directory,
I referenced it in my `_includes/head.html` file.
With a quick refresh of my local Jekyll server and an inspection of a couple of my site's pages,
I could see the Google Analytics `<script>`.
It had worked!

I pushed all of my changes to GitHub and merged with my main branch.
After deployment I checked my live-site and again saw the script.
I felt like I had unlocked a level in my understanding of Jekyll, GitHub Pages, and HTML.

I completed all of this on February 1, 2025—the day after I published [_2024:
Year in Review_]({{ site.baseurl }}{% link _posts/2025-01-31-year-in-review.md %}).
For the last couple of weeks I've been looking at my site's web traffic.
It's been enjoyable to see.
I don't have a lot of visitors; maybe one or two a day with most of them going to my more recent posts.
But it feels good to be seen.

In January 2024, when my site was a few posts old, I added the ability to comment and react to my posts via [giscuss](https://giscus.app/).
After adding Google Analytics to my `_includes/` and letting Jekyll handle the automation,
I figured it was hightime to do the same with my comments.

Yes,
I've literally been copy/pasting an HTML script to the bottom of every post
since I published [_Comments_]({{ site.baseurl }}{% link _posts/2024-01-10-comments.md %}).
It's been tedious, and I've accidentally published multiple times without the script,
having to go back and add it after the fact.
It's not that I didn't want to automate it
—I considered writing a pre-commit hook to check for it—I just didn't know how.

Until now.
> [!NOTE]
> 
> Walk through adding the giscuss `<script>` to `_includes/` and referencing it in `_layouts/post.html`.

Much better.
After testing that I wouldn't lose my existing comments and reactions,
I removed the old `<script>` elements from the bottoms of my existing posts.
Now I can write and publish without having to worry that readers won't be able to leave feedback.

Last year, when I first added the ability to comment, my goal was to get feedback on my posts.
To have conversations with my readers.

After sharing my posts on LinkedIn to spread the word that I have a blog, a weird even occurred:
readers started reacting and writing comments on my LinkedIn post rather than my actual blog posts.

It's kind of funny.
I got through an effort to allow interaction on my site and it turns out all I had to do was share on LinkedIn.
I can think of reasons why this happened:
- readers don't have GitHub accounts so can't comment directly
- the path of least resistance to interact is on LinkedIn where the post was discovered
- etc.

Whatever it is, I welcome it.

I write the posts and share them in an effort to educate, learn, and converse.
It shouldn't matter how my students, teachers, readers,
friends choose to interact as long as I can provide a way to do so.
Comment on LinkedIn.
React on my site.
Whatever you do and where you do it, I see and read them all.
And I appreciate it 🤗.