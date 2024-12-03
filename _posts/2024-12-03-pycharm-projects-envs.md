---
layout: "post"
title: "PyCharm: Projects & Environments"
date: 2024-12-03
---

I use [PyCharm](https://www.jetbrains.com/pycharm/) for most, if not all, of my development.
Professional edition at work.
Community edition for everywhere else.
There are some subtle differences between the two, but [project](https://www.jetbrains.com/help/pycharm/setting-up-your-project.html) and [virtual environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) management are not.

# Projects
When I first started using PyCharm I worked in a single [repo](https://en.wikipedia.org/wiki/Repository_(version_control)).
As my responsibilities increased, I was asked to work on others.
I'd [`git clone`](https://git-scm.com/docs/git-clone) new repos to the same parent directory as my other pre-existing repos
and work away.
>What my directory resembled.
>```text
>📂
>├── 📂 Repo_1
>├── 📂 Repo_2
>├── ...
>└── 📂 Repo_N
>
>```

Over time, I noticed PyCharm was turning into a snail. 🐌
Using the terminal.
Navigating the directory pane.
Running code via the interpreter.
It didn't matter what I did, everything was slow.

I don't remember exactly where I read the suggestion (I'll assume [Stack Overflow](https://stackoverflow.com/questions/tagged/pycharm)),
but someone mentioned treating each repo as its own PyCharm project.
In simpler terms, ths meant opening PyCharm at the _repo_ level, i.e.,
>```text
>❌ 📂  <- not here
>├── ✅ 📂 Repo_1  <- open PyCharm here,
>├── ✅ 📂 Repo_2  <- here,
>├── ...
>└── ✅ 📂 Repo_N  <- or here
>
>```

Doing this reduced the amount of files that PyCharm had to inspect.
The less work PyCharm has to do, the faster it can run.
It also means I'm less to prone to looking at the wrong file/folder by accident.
>[!NOTE]
>If you have multiple _small_ repos this may not be an issue.
>But I still advise considering this approach as it's helped me keep code separate.
