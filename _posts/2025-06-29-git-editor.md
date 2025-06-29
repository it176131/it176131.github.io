---
layout: "post"
title: "Git's Core Editor: (Back to) Vim"
date: 2025-06-29
---

Based on my GitHub history, I probably started using [`git`](https://git-scm.com/) from the [CLI](https://en.wikipedia.org/wiki/Command-line_interface) sometime between 2015 and 2018.
Not sure on an exact date, but I do remember trying to get comfortable with the commands and accidentally entering a
[`vim`](https://www.vim.org/) editor.
More than likely it was because I tried to [commit](https://git-scm.com/docs/git-commit) an [`.ipynb`](https://ipython.org/notebook.html) file with
`git commit -a -m <some commit message>` and hit <kbd>ENTER</kbd> before I got to the `-m` flag.
Coming from the privileged world of "mouse first, keyboard second," I was terrified when I couldn't _easily_ exit or
backout of the editor.

How would you feel if nothing happened when you clicked a spot with your mouse?
Or worse, you tried to type something and the cursor block started moving around the page and then began editing?
I don't remember what I did, but pretty sure I ended up closing the whole CLI down and starting over... this time
carefully avoiding the <kbd>ENTER</kbd> key until _after_ I had typed `-m <some commit message>`.

I continued to work like this for a handful of years, picking up some other `git` commands along the way:
[`git clone`](https://git-scm.com/docs/git-clone), [`git log`](https://git-scm.com/docs/git-log), [`git push`](https://git-scm.com/docs/git-push), [`git pull`](https://git-scm.com/docs/git-pull) [`git remote`](https://git-scm.com/docs/git-remote).
Not a ton, but enough to be useful.

Between 2019 and 2022 I started using the CLI a lot and tried to learn a bit more about the [`git config`](https://git-scm.com/docs/git-config)
settings, especially when it came to working around my employer's firewall.
Understanding how to set and edit environment variables, adding to my system's PATH, downloading certificate packages
and pointing `git` to them.
For the most part I could do this with a mouse and some `git config` options, but at some point I discovered that I
could set my `git` editor and do more at once.

# My Handy Dandy ~~Notebook~~ Notepad
Viewing all of my existing `git config` settings is pretty straightforward; open a git-compatible CLI and type
`git config --list`.
By default, this will show _all_ of your config settings: local (repo specific), global (i.e., user), and system.
If you want to view a specific group of settings, e.g., the local settings, you can add the flag `--local`, as in,
`git config --local --list`.

Editing the config is a bit more involved.
To set a `--global` config option, e.g., `user.name` (useful for signing commit messages 😉):
```shell
# Must use quotes if a space is present.
$ git config set --global user.name "Ian Thompson"
# DEPRECATED --> $ git config --global user.name "Ian Thompson"
```
Want to check the value?
```shell
# Will return an empty string if not set,
# or an error if the section doesn't exist,
# e.g., `git config get --global blah`
$ git config get --global user.name
# DEPRECATED --> $ git config --global user.name`
```
To unset the option:
```shell
$ git config unset --global user.name
# DEPRECATED --> $ git config --global --unset user.name
```
> [!NOTE]
> If you set a `--global` config option, then you must specify the option as `--global` when you unset it, otherwise it
> may not work.

This is all fine, but what if you're not quite comfortable with the CLI yet?
Or you want to use your mouse a bit more?
We can allow that by setting the `core.editor` to `notepad`, the classic text editor.
```shell
# Set the editor with the following command.
$ git config --global core.editor notepad
```
Then to make edits to the config (`--global` for this example), run the following:
```shell
$ git config --global --edit
```
This will open your `git config` settings in a notepad editor, allowing the use of your trusty mouse.