---
layout: "post"
title: "PyCharm: Projects & Environments"
date: 2024-12-03
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
>If you have multiple _small_ repos this may not be an issue.
>But I still advise considering this approach as it's helped me keep code separate.

# Environments
I wrote a [blog post](https://medium.com/@ianiat11/we-recommend-creating-an-environment-da38af0cecbb) a couple years ago
that briefly covers two kinds of virtual environments:
[`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) and [`venv`](https://docs.python.org/3/library/venv.html).
If you read it you may notice that I'm not a big fan of `conda`, so we're not going to talk about here.
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
1. Open PyCharm's settings (find the cog symbol ⚙️ and select "settings" or hit the correspondign [hotkey](https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html)).
2. Click "Project: <your project/repo name>" in the left pane
3. Click Python Interpreter
4. Click "Add Interpreter" in the top right of the window (should be in <span style="color:blue">blue</span>)
5. Click "Add Local Interpreter..."
6. Click "Select existing"
7. Set the Path field to the "python.exe" in your project's environment (should be something like "./env/Scripts/python.exe")
8. Click "OK" all the way back to the settings menu and close it.

You should now be able to run python within PyCharm using the ["Run" option](https://www.jetbrains.com/help/pycharm/running-without-any-previous-configuring.html).

# Gotcha
Setting the project interpreter may lead to weird quirk in the terminal.
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
3. Click "Terminal"
4. Scroll to the bottom and uncheck "Activate virtualenv"
5. Click "Apply"
6. Click "OK"
7. Restart your terminal

Voila! Now you can activate your environment from the terminal and still use your other commands.

If you'd like to persist this setting to every _new_ project your create, you can do so by editing the project settings.
1. Go to File > New Projects Setup > Settings for New Projects...
2. Repeat the steps we took to uncheck the "Activate virtualenv" configuration.

# Running Multiple Projects