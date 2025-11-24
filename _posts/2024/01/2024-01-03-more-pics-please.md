---
layout: "post"
title: "More Pictures Please"
date: 2024-01-03
images: "/assets/images/2024-01-03-more-pics-please/MeAndWillie.jpg"
---

As I shared my [first "official" post]({{ site.baseurl }}{% link _posts/2024-01-01-new-year.md %}) to some friends and family, I realized it would be better if I had included pictures.
Since I don't exactly know how to add pictures yet, this post will be more of a follow-along.
That is you, the reader, will follow me, Ian, as I learn how to add pictures (and video?) to my posts.
Here goes nothing!

# Google Search
I started off with a Google search for "jekyll add images".

> BTW<br>
> The software I'm using to build my blog is called [`jekyll`](https://jekyllrb.com/).
> If you want a `jekyll` tutorial I highly recommend [this series](https://youtube.com/playlist?list=PLLAZ4kZ9dFpOPV5C5Ay0pHaa0RJFhcmcB&si=4RfenoUQySjThNak) by [Giraffe Academy](https://www.youtube.com/@GiraffeAcademy) on YouTube.

The result that caught my immediate attention was ["Learn how to add featured images to your posts"](https://talk.jekyllrb.com/t/learn-how-to-add-featured-images-to-your-posts/4852).
The description mentioned adding images to the top of a blog post.
While that isn't _exactly_ what I want, I figured it'd be a good place to start.
Maybe I could hack my way to a solution 😉.

I decided to watch ["Part 1: Add a featured image to your posts"](https://youtu.be/6oKO-7gsM4s?si=ip71pE4il6roRLhN), and after making it through the first couple minutes, I made it to [the good stuff](https://youtu.be/6oKO-7gsM4s?t=116&si=sqFIUYU2cPcHdE8K).
Based on my (very little) knowledge of `jekyll`, I decided to create a directory/folder called "_assets" instead of "assets" as seen in the video.
I thought this was good practice, but it would end up biting me in the butt later 😒.

Proceeding with the video, I created a directory called "images" inside "_assets", downloaded a nice picture of me and my oldest cat, Willie, and dropped it into "_assets/images/".
Next, I added the following `yaml` to the front matter of this post:
```yaml
images: "/_assets/images/MeAndWillie.jpg"
```

To get the image to show up _somewhere_ in my post, I put the following `markdown` at the bottom of this post.
<!-- {%raw%} -->
```markdown
![Me and Willie]({{ page.images | relative_url }})
```
<!-- {%endraw%} -->

It didn't work 😑.
Back to Google...

# Help
Back in the search results, I found ["I cannot get an image to display"](https://talk.jekyllrb.com/t/i-cannot-get-an-image-to-display/850).
It seems other readers of the ["Learn how to add featured images to your posts"](https://talk.jekyllrb.com/t/learn-how-to-add-featured-images-to-your-posts/4852) article were having a similar problem.
Scrolling down to almost the end, I found my [solution](https://talk.jekyllrb.com/t/i-cannot-get-an-image-to-display/850/10):
> just for clarification: Jekyll does not ignore the underscores, it ignores all content (files or folders)<br>
> beginning with an underscore.<br>
> In all probability everyone knew that already :).
 
Thank you, [michaelbach](https://talk.jekyllrb.com/u/michaelbach).
I guess I'm not included in "everyone".
Butt bitten 🍑.

I refactored (computer-speak for edited/renamed 🤓) my "_assets" directory to "assets", and updated the front matter at the top of the post to:
```yaml
images: "/assets/images/MeAndWillie.jpg"
```

At last!
A picture of me and Willie 😍😻!

![Me and Willie]({{ page.images | relative_url }})

Now I can add pictures to my other posts.
Watch out for edits!