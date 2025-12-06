---
layout: "post"
title: "Rebase More Efficiently—Update the Index"
date: 2025-11-29
images: "/assets/images/2025-11-30-update-index"
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

On my feature branch—`new-feat`—I find the commit where I first created _2025-11-30-new-file.txt_,
```shell
$ commit=$(git log --format=%h --reverse -- 2025-11-30-new-file.txt | head -1)
```
and rebase:
```shell
git rebase -i $commit~
```

In the rebase editor I replace _pick_ for _e_ (or _edit_) on the first commit,
```diff
- 1   pick 91335bc # Tracking new file for blog purposes.
+ 1   e 91335bc # Tracking new file for blog purposes.
    1 pick 56846f2 # Added some text to start building up the commit history.
    2 pick d0e2157 # Another commit for a bit more history.
    3 pick d21596e # Last commit before rebasing and attempting to cause a merge conflict.
```
save, and quit.
I'm now right between commits `91335bc`, where I created the file,
and `56846f2`, the commit that follows immediately after.

I create the new subdirectory `2025/11/`, `git mv` the file,
and amend the changes to the previous commit with the `--amend` flag.
```shell
$ mkdir 2025/11/ -p
$ git mv 2025-11-30-new-file.txt 2025/11/2025-11-30-new-file.txt
$ git commit --amend  # Recall that `git mv` automatically stages the changes for you; no need to `git add` or use the `-a` flag.
```

With nothing left to do, I continue the rebase,
```shell
$ git rebase --continue
```
and there's the merge conflict.
```text
CONFLICT (modify/delete): 2025-11-30-new-file.txt deleted in HEAD and modified in 56846f2 (Added some text to start building up the commit history.).  Version 56846f2 (Added some text to start building up the commit history.) of 2025-11-30-new-file.txt left in tree.
error: could not apply 56846f2... Added some text to start building up the commit history.
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
Could not apply 56846f2... # Added some text to start building up the commit history.
```

What do I do now?
First, it'd probably be good to draw a picture of what the conflict is telling us.
<center>
    <figure>
        <img src="{{ page.images | relative_url }}/initial-branch.png">
        <figcaption>The initial branch</figcaption>
    </figure>
</center>
This is what the initial branch looked like before we rebased and attempted to rewrite history.

During the rebase we went back to commit `91335bc`,
`git mv`-ed _2025-11-30-new-file.txt_ from the root directory to the new `2025/11/` directory,
and amended commit `91335bc` with that change.
This results in a new commit hash replacing `91335bc` → `91335bc*`.
<center>
    <figure>
        <img src="{{ page.images | relative_url }}/amended-commit.png">
        <figcaption>The new hash</figcaption>
    </figure>
</center>

Before we run `git rebase --continue`,
our [`HEAD`](https://git-scm.com/book/ms/v2/Git-Internals-Git-References#ref_the_ref) is at the amended commit,
`91335bc*`.
<center>
    <figure>
        <img src="{{ page.images | relative_url }}/head-loc.png">
        <figcaption>`91335bc*` ↔ `HEAD`</figcaption>
    </figure>
</center>

The contents of which are,
```text
tmp/
├── 2025
│   └── 11
│       └── 2025-11-30-new-file.txt
└── README.md
```

When we try to continue the rebase, we run into the merge conflict:
```shell
$ git rebase --continue
CONFLICT (modify/delete): 2025-11-30-new-file.txt deleted in HEAD and modified in 56846f2 (Added some text to start building up the commit history.).  Version 56846f2 (Added some text to start building up the commit history.) of 2025-11-30-new-file.txt left in tree.
error: could not apply 56846f2... Added some text to start building up the commit history.
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
Could not apply 56846f2... # Added some text to start building up the commit history.
```

Why?
If we look at the current directory structure in the middle of the conflict we can see part of the issue:
```text
tmp/
├── 2025
│   └── 11
│       └── 2025-11-30-new-file.txt
├── 2025-11-30-new-file.txt
└── README.md
```

_2025-11-30-new-file.txt_ is in two different places,
one is from `HEAD` and the other is where `56846f2` expects the file to be.
```