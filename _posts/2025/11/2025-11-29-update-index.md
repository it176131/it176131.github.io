---
layout: "post"
title: "Rebase More Efficiently—Update the Index"
date: 2025-11-29
---

Git offers a lot of functionality.
Most users probably hover around the basics—[`git clone`](https://git-scm.com/docs/git-clone),
[`git branch`](https://git-scm.com/docs/git-branch), [`git checkout`](https://git-scm.com/docs/git-checkout),
[`git add`](https://git-scm.com/docs/git-add), [`git commit`](https://git-scm.com/docs/git-commit),
[`git push`](https://git-scm.com/docs/git-push), [`git pull`](https://git-scm.com/docs/git-pull)—and don't use much else.
But for the fraction who decide to venture a bit further either out of curiosity or necessity,
they're bound to learn about [`git rebase`](https://git-scm.com/docs/git-rebase) and encounter a [merge conflict](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merge_conflicts) or two.

I recently restructured my blog's repo,
moving all of my posts into respective YYYY/MM/ directories instead of all living at the same level.
It took a few PRs (`jekyll` wasn't playing nicely),
but I got it working and everything was republished without altering the posts' URLs.

After `git pull`-ing and updating my local main branch, I switched back to the blog post I was working on prior.
This branch was made before the restructure, and so the post wasn't in the correct (new) subdirectory.
As I was already a few commits in and didn't want to add a new one _simply_ to move it to a subdirectory,
I decided to `git rebase` and edit the initial commit where I created the file.
This would allow me to move the file to its respective YYYY/MM/ directory, making it look like it was always there.
With a quick `git rebase -i <initial-commit-hash>~`,
a couple [vim](https://www.vim.org/) commands, and a `git mv`, I'd changed history.
To get the remaining commits to follow suit I ran `git rebase --continue`... merge conflict.
🤬

# Recreating the problem
I've resolved this merge conflict two different ways,
both of which would be easier to understand if I recreated the problem and let you follow along.
Let's start by making a new local repo and adding a README.md.
```shell
# Somewhere on your machine...
$ mkdir tmp  # Make the directory.
$ cd tmp
$ git init  # Convert it to a repo.
$ touch README.md  # Create the README.md and track it with git.
$ git add README.md && git commit
```

We'll be smart git users and create a new branch rather than directly editing the main/master/primary/whatever branch.
```shell
$ git checkout -b new-feat
```

Add a new file and track it.
```shell
$ touch 2025-11-30-new-file.txt
$ git add 2025-11-30-new-file.txt && git commit
```

Now we need to make a few commits to build out the history.
```shell
# Write some text to the file and commit the changes.
$ echo "test" > 2025-11-30-new-file.txt
$ git commit -a
# Add some more text to the bottom, commit again.
$ echo "abc 123" >> 2025-11-30-new-file.txt
$ git commit -a
# Maybe one more... 🌳
$ echo "happy little trees" >> 2025-11-30-new-file.txt
$ git commit -a
```

This is the part where I decide to restructure the repo.
Instead of having all files at the same directory level,
```text
tmp/
├── 2025-11-30-new-file.txt
└── README.md
```
I want to have them in a subdirectory structure organized by year and month.
```text
tmp/
├── 2025
│   └── 11
│       └── 2025-11-30-new-file.txt
└── README.md
```

# Solutions
There are two different ways I could do this:
1. `git mv` the file and commit the changes at the end of the current branch
2. `git rebase` and edit the initial commit where I created the file making it look like the proposed file structure always existed

The first option is fine,
but it adds a commit and makes the git history look as if we made the decision to modify the directory structure midway through the development of our feature branch.
The second option repurposes the initial commit, but is a bit more involved.
I'm choosing the second option because I want a cleaner history.