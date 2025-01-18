---
layout: "post"
title: "Actions & Workflows: Automatically Updating My GitHub Profile with Recent Blog Posts"
date: 2025-01-18
---

First post of 2025!

I ended 2024 with my post, [_pydantic-xml: Parsing My RSS Feed_]({{ site.baseurl }}{% link _posts/2024-12-23-pydantic-xml.md %}),
and mentioned that I was trying to add my most recent blog post to my GitHub profile using a custom GitHub action and workflow.
I'm happy to share that after a couple of weeks, I figured it out. 😎

Rather than walk through all the struggles I experienced,
I'll give a high level overview of what I have now, and how everything interacts with each other.

# The files
```
📂 it176131.github.io
└── 📂 .github
    └── 📂 actions
        └── 📂 recent-posts
            ├── 🔧 action.yml
            ├── 🐋 Dockerfile
            ├── 🐍 main.py
            └── 📄 requirements.txt

📂 it176131
└── 📂 .github
    └── 📂 workflows
        └── 🔧 recent-posts.yml
```

As I mentioned, I wanted to add blog posts from my [blog](https://it176131.github.io/) to my [GitHub profile](https://github.com/it176131).
To keep things organized, I decided to keep the [_action_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#actions) in the [blog repo](https://github.com/it176131/it176131.github.io), and the [_workflow_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#workflows) in the [profile repo](https://github.com/it176131/it176131).