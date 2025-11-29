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