---
layout: "post"
title: "Innovation Week: Incubation à la Monorepo"
date: 2025-03-28
---

In an attempt to promote collaboration, I created a [monorepo](https://en.wikipedia.org/wiki/Monorepo) for "innovation week."
Innovation week happens four times a year at the end (or beginning) of each quarter.
The purpose is to allow people to work on a project that could benefit the company without sponsorship.

"Sponsorhsip" means a project is being funded by someone in the company—usually a people-leader like a manager,
director, VP, or C-suite member.
Individual contributors (ICs) like myself can't sponsor projects because,
well, we don't have allocated funds to do such a thing.
Hence, the beauty of innovation week.

In past innovation weeks, normally I only hear about what others are working on at stand-up meetings.
It's almost the equivalent of a 30-second teaser trailer minus any visual aid.
For projects that last longer than a week, stand-up briefings start to make sense.
Over the course of 10–15 30-second teasers, I can kind of get an idea of what someone is working on
and maybe offer some userful assistance when they mention a blocker or technical problem.

Unfortunately, innovation week doesn't allow for this because it's just that—a week.
Five 30-second teasers isn't enough for me (anyone?) to grasp what someone is trying to achieve.
It also doesn't help get projects out of the "idea" phase and into the "sponsored" phase.
And like so many innovation week ideas from the past,
a lot of them end up in repo purgatory where they await resurrection by their creator in minimum three months...
or get deleted and sent to an unmarked grave.
It's quite depressing honestly.

But the monorepo could help alleviate some of this!
Without forcing anyone to change their workflow (hopefully 🤞),
the monorepo can be a safe place for ideas to come together and be seen by other contributors.
It removes the silo-effect of every idea having its own repo
and being nearly unfindable, while also maintaining some form of separation via dedicated subdirectories.
It also acts as a small portfolio in case a people-leader comes along in three years
and wants to know if we can solve a problem that one of us just so happened to ideate on.
Anything is possible.

I had the idea for the monorepo a few days ago and have since shared it with my immediate team.
Just before writing this, I thought about an idea for the week to work on,
and then it hit me—I already have code in repo purgatory that I could resurrect!
But how do I keep it alive, or at least give it a properly marked grave in case it dies again?
Enter the monorepo.

I had already made a decent number of commits to my recently resurrected repo and didn't want to lose the history.
At the same time, I needed to move the code to the monorepo so it would be easier to find in the future.
How do I maintain history and move my repo into a subdirectory of the monorepo?

After some Googling I came across this Stack Overflow question,
[_Merge two Git repositories without breaking file history_](https://stackoverflow.com/questions/13040958/merge-two-git-repositories-without-breaking-file-history),
from 2012.
Of course someone else has already tried to do this.
After some reading and scrolling,
I found [an answer](https://stackoverflow.com/questions/13040958/merge-two-git-repositories-without-breaking-file-history/62096626#62096626)
I liked and could understand.

I'm going to use the example code from the answer as my base, and include some extra details along the way.
First, I made sure I had local clones of both my soon-to-be-resurrected repo and the monorepo.
```shell
# Somewhere on my local machine...
$ git clone https://url/path/to/repo/called/not-dead.git  # to be resurrected
$ git clone https://url/path/to/repo/called/mono.git  # the monorepo
```

> [!NOTE]
> 
> If you already have local clones, make sure you've synced your history with your remote sources.
> You can do that with:
> ```shell
> $ cd your-local-repo/
> $ git pull  # I prefer `git pull --rebase` as I don't want to add a merge commit. It keeps my history linear and clean.
> ```

With both repos updated it's time to pack up `not-dead` into a subdirectory and move it into `mono`.
```shell
$ cd not-dead/
$ git filter-repo --to-subdirectory-filter not-dead
$ cd ../
```
> [!NOTE]
> 
> To use `git filter-repo` you have to install it.
> If you're a Python user you can `pip install git-filter-repo`.
> Otherwise checkout [_How do I install it?_](https://github.com/newren/git-filter-repo?tab=readme-ov-file#how-do-i-install-it) on the [`git-filter-repo` repo](https://github.com/newren/git-filter-repo).

Before we continue let's see what `git filter-repo` did to my `not-dead` repo.
```shell
$ ls not-dead/
# not-dead/
```
Using the `--to-subdirectory-filter` flag with argument "not-dead"
took the contents of my `not-dead` repo and moved it all inside a subdirectory of the same name...
all while preserving the history.
```shell
$ cd not-dead/
$ git log
# Lots of commit logs...
```

Pretty nifty!
Now to move it into the monorepo.
```shell
# Assuming we're starting in the not-dead/ repo...
$ cd ../mono
$ git remote add not-dead ../not-dead
$ git fetch not-dead
$ git merge --allow-unrelated-histories not-dead/master  # or not-dead/main if that's the name of your primary branch
$ git remote remove not-dead
```

<blockquote>
<details>
<summary>⚠️ Using Git LFS? Experiencing an issue? Expand me for a potential solution!</summary>

If you tried to move a repo with LFS tracked files to the monorepo and got some kind of LFS error message, don't fret.
I, too, hit a snag when I ran the following:
```shell
$ git merge --allow-unrelated-histories not-dead/master
```

The error I received looked something like this:
```text
Error downloading object: <some-file.some-extension> (<some-hash>):
Smudge error:
Error downloading <some-file.some-extension>
(<some-hash>):
[<some-hash>]
Object does not exist on the server or you don't have permissions to access it:
[404] Object does not exist on the server or you don't have permissions to access it
```

When this error occurs, it can appear like everything is fine.
Your files will appear to have made it the monorepo as expected,
but if you check your `git log` you may notice a lack of history related to your LFS-tracked repo.
Yes, the files made it, but not their commits.
And the whole point of doing all this was to bring them along for the ride!
So what do we do?

_After_ running `git fetch not-dead` and _before_ running `git merge --allow-unrelated-histories not-dead/master`,
we need to fetch all the LFS objects for our `not-dead/master` branch.
> At this point if you need to back-track you can.
> Delete your equivalent of the new `not-dead/` directory in the monorepo and all its contents.
> This will get you back to just before running `git fetch not-dead`.

We run the following to fetch our `not-dead` LFS objects and bring them to our monorepo:
```shell
# From the monorepo...
$ git lfs fetch not-dead master
```

Now when we run `git merge --allow-unrelated-histories not-dead/master` we won't get the LFS error.
Only smiles.
🙂
</details>
</blockquote>

And voilà!
We've successfully moved my `not-dead` repo into the monorepo and maintained history.
The only thing
I might do now is move the `not-dead/` directory to a dedicated subdirectory for all innovation week ideas.
I'll call it "libs," but you could also call it "repos," "packages,", "ideas"... you get the point.
```shell
# We're still inside the mono/ repo...
$ mkdir libs
$ mv not-dead libs/
$ git add . && git commit  # Don't forget to commit the directory movement!
```

# Three years later...
The `monorepo` has become home to many innovative ideas and now a people-leader wants to sponsor one of them.
Hooray!
🥳
What do we do now?
We move the idea out of the monorepo and into its own repo of course!
But not without its commit history.
We can do this using `git filter-repo` (again).

To ensure we don't destroy the monorepo we'll make a fresh clone,
but this time we'll name it whatever our new repo is going to be called.
I'll call it "sponsored."
```shell
# Make sure the primary branch of mono is synced with its origin!
$ cd mono/
# From the primary branch, main/master/whatever...
$ git pull  # or `git pull --rebase`
$ cd ../
$ git clone mono sponsored --no-local
```
> [!NOTE]
> 
> The `--no-local` flag is important!
> When git performs a local clone it defaults to optimized behaviors that save space where available.
> We don't want this.
> By supplying `--no-local` we're essentially telling git to perform the clone as if it were coming from a URL.

We now have a fresh local clone of `mono` but with the name "sponsored."
To dedicate this new clone to the sponsored project, we'll filter out everything unrelated to it.
```shell
$ cd sponsored
$ git filter-repo --path libs/not-dead  # or whichever directory earned sponsorship...
```

If you look at the contents of `sponsored/` you'll notice everything is gone save the directory `libs/not-dead/`.
Now if it were me I'd bring the contents of `libs/not-dead/` to the root level
as there's no need for nested-ness in its own directory.
I can do this with the following:
```shell
$ git filter-repo --path-rename libs/not-dead/:  # the colon (:) is needed!
```

Now if we check the contents we should see whatever was in `libs/not-dead` at the root of `sponsored/`.

> [!NOTE]
> 
> If you want to do this all in one command, you can, chaining `--path ... --path-rename ...`.
> Or you can use the shortcut `--subdirectory-filter` like so:
> ```shell
> # Assuming we start from a fresh clone...
> $ cd sponsored
> $ git filter-repo --subdirectory-filter libs/not-dead/
> ```
> 
> Checking the contents of `sponsored/` you'll see the same results.

Now we have a filtered repo dedicated to the sponsored project with history.
Next we should add a remote location so its viewable by other contributors and not living on our local machine.
To do that, make a new repo on your desired platform, e.g. GitHub, and make srue there's nothing in it.
No README.md, .gitignore, nothing.
After it's been created, get the URL as if you were going to clone it.
Go back to your terminal and run the following:
```shell
# From inside sponsored/
$ git remote add origin <URL>
```

This connects your local repo to the remote repo you just created.
Now push your history (with force if necessary):
```shell
$ git push --set-upstream origin master  # with `--force` if needed. 
```

If this doesn't work, e.g. you have branch policies in place preventing you from pushing directly to the primary branch
(normally a good idea!), you can change branch names, push,
then open a Pull Request (PR) to merge your local repo with the remote.
For example:
```shell
$ git branch -m new-branch
$ git push -u origin new-branch  # followed by a PR of new-branch -> master
```

And that's it!
Kind of.
The sponsored project has its own repo, but it still exists in the monorepo too.
To celebrate its graduation and give it a final sendoff we should do the following:
1. Update the monorepo README.md to say `not-dead` was sponsored (maybe with a date and link to the new repo?)
2. Delete the original `libs/not-dead/` directory to keep other contributors from diverging its history.

Now we're done.
😁