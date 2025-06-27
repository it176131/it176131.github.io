---
layout: "post"
title: "Git's Core Editor: (Back to) Vim"
date: 2025-06-27
---

Based on my GitHub history, I probably started using [`git`](https://git-scm.com/) from the [CLI](https://en.wikipedia.org/wiki/Command-line_interface) sometime between 2015 and 2018.
Not sure on an exact date, but I do remember trying to get comfortable with the commands and accidentally entering a
[`vim`](https://www.vim.org/) editor.
More than likely it was because I tried to [commit](https://git-scm.com/docs/git-commit) an `.ipynb` file with `git commit -a -m <some commit message>`
and hit <kbd>ENTER</kbd> before I got to the `-m` flag.
Coming from the privileged world of "mouse first, keyboard second," I was terrified when I couldn't "easily" exit or
backout of the editor.

How would you feel if nothing happened when you clicked a spot with your mouse?
Or worse, you tried to type something and the cursor block started moving around the page and then began editing?
I don't remember what I did, but pretty sure I ended up closing the whole CLI down and starting over... this time
carefully avoiding the <kbd>ENTER</kbd> key until _after_ I had typed `-m <some commit message>`.

I continued to work like this for a handful of years, picking up some other `git` commands along the way:
[`git clone`](https://git-scm.com/docs/git-clone), [`git log`](https://git-scm.com/docs/git-log), [`git push`](https://git-scm.com/docs/git-push), [`git pull`](https://git-scm.com/docs/git-pull) [`git remote`](https://git-scm.com/docs/git-remote).
Not a ton, but enough to be useful.

Between 2019 and 2022 I tried to learn a bit more about the [`git config`](https://git-scm.com/docs/git-config) settings, especially when it came to
working around my employer's firewall.
Understanding how to set and edit environment variables, adding to my system's PATH, downloading certificate packages
and pointing `git` to them.
For the most part I could do this with a mouse and some `git config` options, but at some point I discovered that I
could set my `git` editor and do more at once.