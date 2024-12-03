---
layout: "post"
title: "PyCharm: Projects & Environments"
date: 2024-12-03
images: "/assets/images/2024-12-03-pycharm-project-envs"
---

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>

I use [PyCharm](https://www.jetbrains.com/pycharm/) for most, if not all, of my development.
Professional edition at work.
Community edition everywhere else.
There are some subtle differences between the two—[project](https://www.jetbrains.com/help/pycharm/setting-up-your-project.html) and [virtual environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) management aren't one them.

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
```text
❌ 📂  <- not here
├── ✅ 📂 Repo_1  <- open PyCharm here,
├── ✅ 📂 Repo_2  <- here,
├── ...
└── ✅ 📂 Repo_N  <- or here

```

Doing this reduced the amount of files that PyCharm had to inspect.
The less work PyCharm has to do, the faster it can run.
It also means I'm less to prone to looking at the wrong file/folder by accident.
Ah...
Modularity.
🧘
>[!NOTE]
> 
>If you have multiple _small_ repos this may not be an issue.
>But I still advise considering this approach as it's helped me keep code separate.

# Environments
I wrote a [blog post](https://medium.com/@ianiat11/we-recommend-creating-an-environment-da38af0cecbb) a couple years ago
that briefly covers two kinds of virtual environments:
[`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) and [`venv`](https://docs.python.org/3/library/venv.html).
If you read it you may notice that I'm not a big fan of `conda`, so we're not going to talk about it here.
Instead we'll use old faithful—`venv`

Managing repos as separate projects is great for modularity.
Having a dedicated environment for each project may help too.
Or at least that's what I do.

Let me share a scenario that both myself and at least one of my colleagues has experienced:
>I have $N$ repos with different requirements—various packages, maybe even different Python versions.
>To work across different repos I have to switch between the environments.
>Unfortunately, I sometimes forget that I've activated one repo's environment and install another repo's requirements.
>This may lead to conflicting package versions, amongst other things.
>It's pretty easy to reset an environment back to its repo's requirements, but also extremely tedious.
>How can I keep my environments and repos in-sync?
>
>Here is the existing layout:
>```text
>📂
>├── 🔧 env_1
>├── 🔧 env_2
>├── ...
>├── 🔧 env_N
>├── 📂 Repo_1
>├── 📂 Repo_2
>├── ...
>└── 📂 Repo_N
>
>```

From the get-go we could move the environments to their respective repos.
```text
📂
├── 📂 Repo_1
│   ├── 🔧 env_1
│   └── ...
├── 📂 Repo_2
│   ├── 🔧 env_2
│   └── ...
├── ...
└── 📂 Repo_N
    ├── 🔧 env_N
    └── ...

```
This would add a degree of separation between them as well as allow us to open the repos as PyCharm projects.
Opening repos as projects keeps us from activating other environments because we won't be able to see them
(unless you `cd ..` then `ls` 😜).

# Virtual Environments As Interpreters
My workflow consists of opening a repo as a project,
then activating the local environment via `git-bash` (or whatever CLI you prefer).
This does not, however, allow you to run scripts by default.
To do that you'll need to configure the project's interpreter by pointing it to your local environment.

I believe this is nearly automatic in newer versions of PyCharm, but if you want/need to do it manually, here's how:
1. Open PyCharm's settings (find the cog symbol ⚙️ and select "settings" or hit the corresponding [hotkey](https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html)).
>![settings-button]({{ page.images | relative_url }}/settings1.png)
2. Click "Project: <your project/repo name>" in the left pane
>![settings-button]({{ page.images | relative_url }}/settings2.png)
3. Click "Python Interpreter"
>![settings-button]({{ page.images | relative_url }}/settings3.png)
4. Click "Add Interpreter" in the top right of the window (should be in <span style="color:blue">blue</span>)
>![settings-button]({{ page.images | relative_url }}/settings4.png)
5. Click "Add Local Interpreter..."
>![settings-button]({{ page.images | relative_url }}/settings5.png)
6. Click "Select existing"
>![settings-button]({{ page.images | relative_url }}/settings6.png)
7. Set the Path field to the "python.exe" in your project's environment (should be something like "./env/Scripts/python.exe")
>![settings-button]({{ page.images | relative_url }}/settings7.png)
8. Click "OK" all the way back to the "Python Interpreter" menu.
>![settings-button]({{ page.images | relative_url }}/settings8.png)
9. **BONUS** You can associate this virtual environment to the current project (hiding it when you view settings in other projects) by clicking the interpreter drop-down, selecting "Show All", then selecting the checkbox, "Associate this virtual environment with the current project".
>![settings-button]({{ page.images | relative_url }}/settings9.png)
> 
>![settings-button]({{ page.images | relative_url }}/settings9.5.png)

You should now be able to run python within PyCharm using the ["Run" option](https://www.jetbrains.com/help/pycharm/running-without-any-previous-configuring.html).

# Gotcha
Setting the project interpreter may lead to a weird quirk in the terminal.
Here's how to check for it.
1. Open your prefered CLI within PyCharm (I use `git-bash`).
2. Activate your environment how you normally would (`source env/Scripts/activate` for `venv` users)
3. Try to use any bash/CLI commands such as `pwd` or `ls`

If these steps result in an error message like this:
>```shell
>$ source env/Scripts/activate
>bash: cygpath: command not found
>```

or this:
>```shell
>$ ls
bash: ls: command not found
>```

Then you have a terminal setting configured that you'd probably like to unset.
1. Open the settings window again
2. Navigate to "Tools" in the left pane
>![settings-button]({{ page.images | relative_url }}/terminal2.png)
3. Click "Terminal"
>![settings-button]({{ page.images | relative_url }}/terminal3.png)
4. Scroll to the bottom and uncheck "Activate virtualenv"
>![settings-button]({{ page.images | relative_url }}/terminal4.png)
5. Click "Apply"
6. Click "OK"
7. Restart your terminal

Voila! Now you can activate your environment from the terminal and still use your other commands.

If you'd like to persist this setting to every _new_ project your create, you can do so by editing the project settings.
1. Go to File > New Projects Setup > Settings for New Projects...
>![settings-button]({{ page.images | relative_url }}/project1.png)
2. Repeat the steps we took to uncheck the "Activate virtualenv" configuration.

# Accessing Your Other Projects
I'd like to share one more thing before we part: how to access your other projects.

We've made our PyCharm workflow a bit more modular
by treating each repo as its own project and dedicating a virtual environment to it.
PyCharm makes it easy for us to switch projects without leaving the curernt one.

At the top left of the window there's the name of our current project:
>![settings-button]({{ page.images | relative_url }}/multi1.png)

This is a drop-down menu.
Clicking it will show us all of our currently registered projects.
>![settings-button]({{ page.images | relative_url }}/multi2.png)

When we click any of them we're greeted with an option menu:
>![settings-button]({{ page.images | relative_url }}/multi3.png)

- "This Window" will replace your current project with the one you selected.
>I use this when I'm done working in the current project.
- "New Window" will open a new PyCharm instance with the project you selected.
>I use this one if I want to work on two projects at the same time, e.g., one project depends on the other. 
- "Attach" will all you to view both projects within the current PyCharm instance
>This is similar to what we've been moving away from—one directory to rule them all.
> I rarely use this option.
- "Cancel"... you know what that does 😜

<script src="https://giscus.app/client.js"
        data-repo="it176131/it176131.github.io"
        data-repo-id="R_kgDOK1ukqg"
        data-category="Announcements"
        data-category-id="DIC_kwDOK1ukqs4CcOnS"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>