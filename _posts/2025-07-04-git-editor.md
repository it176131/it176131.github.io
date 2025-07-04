---
layout: "post"
title: "Git's Core Editor: (Back to) Vim"
date: 2025-07-04
images: "/assets/images/2025-07-04-git-editor"
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
`git config list`.
By default, this will show _all_ of your config settings: local (repo specific), global (i.e., user), and system.
If you want to view a specific group of settings, e.g., the local settings, you can add the flag `--local`, as in,
`git config list --local`.

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
$ git config set --global core.editor notepad
```
Opening the config (`--global` for this example) for mass edits then becomes as simple as:
```shell
$ git config edit --global
```
This will open your `git config` settings in a notepad editor, allowing the use of your trusty mouse.

# More Detail, Better Commits
In 2022, I changed jobs and got a new machine.
While installing the latest version of `git`—_not version 2.50.0, by the way_—I noticed a setting I hadn't before:

|-------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| ![Git Default Editor 1]({{ page.images | relative_url }}/choose-default-editor.png) | ![Git Default Editor 2]({{ page.images | relative_url }}/editor-options.png) |

You can set the default editor (i.e., `core.editor`) at installation!
That's convenient.
Obviously I picked `notepad` and continued on.

A few months into the new gig, I demoed some work with a group of colleagues and had written some code that I
thought was worth keeping.
I switched to my CLI and wrote:
```shell
$ git commit -a -m "some commit message related to what my code does"
```
And before I hit <kbd>ENTER<kbd>, one of the veterans on my team stopped me.
"Leave off the '-m' so you can write a more detailed commit message.
It'll help you and future developers understand more about what you did and why."

I was confused—and annoyed; my flow had been interrupted—but I tried it.
```shell
$ git commit -a
```
Notepad opened with something like this:
```text

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch git-editor
# Your branch is up to date with 'origin/git-editor'.
#
# Changes to be committed:
#	modified:   _posts/2025-07-04-git-editor.md
#

```

"Okay, now add a brief summary of what your committed work does—_and why_—to the top of the editor.
Then go down to the 'Changes to be committed' section and uncomment the 'modified' line.
You can add another file-specific summary under each file path saying what happened in it."

"Why can't I just use the '-m' from the CLI?" I really wanted to commit my work and move on.

"This allows you to keep a more detailed change log, which helps others understand your reasoning without having to read
your code line-by-line."

"But nobody uses that," I was getting frustrated.

"I do."

Stalemate.
I didn't want to change my process.
Anger.
I didn't want to do more work.
End demo.

I _obsessively_ thought about what my colleague had shown me over the next few days.
Google searches of "how to write a better commit message," and "use the git log better."
In the end I determined that most people wrote commit messages like I did—'-m' style.
But something deep inside told me to try my colleague's method.
I changed my style, and to my honest surprise reading over my logs is actually enjoyable now.
