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
To keep things organized,
I decided
to put the [_action_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#actions) in the [blog repo](https://github.com/it176131/it176131.github.io),
and the [_workflow_](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions#workflows) in the [profile repo](https://github.com/it176131/it176131).
```
📂 it176131.github.io
└── 📂 .github
    └── 📂 actions
        └── 📂 recent-posts  # The action and all its requirements
            ├── 🔧 action.yml
            ├── 🐋 Dockerfile
            ├── 🐍 main.py
            └── 📄 requirements.txt

📂 it176131
└── 📂 .github
    └── 📂 workflows
        └── 🔧 recent-posts.yml  # The workflow file
```

There are three [types of actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#types-of-actions):
[Docker container](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#docker-container-actions), [JavaScript](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#javascript-actions), and [composite actions](https://docs.github.com/en/actions/sharing-automations/creating-actions/about-custom-actions#composite-actions).
I opted to use a [Docker container](https://www.docker.com/resources/what-container/) because:
1. I don't know enough [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
to be comfortable writing an action from scratch, and
2. This is my first custom action and workflow, so I don't think I need to create a _composite action_ just yet.

Using a Docker container also allows me
to use my preexisting Python script from the last [post]({{ site.baseurl }}{% link _posts/2024-12-23-pydantic-xml.md %}).


# I'll be using this later
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
├── 📂 .github
│   └── 📂 workflows
│       └── 🔧 recent-posts.yml
└── 📓 README.md  # My "profile"
```
