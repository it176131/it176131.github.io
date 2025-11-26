---
layout: "post"
title: "Notebook ➡️ Post"
date: 2024-03-12
---

After I published my [post introducing the Stack Overflow API]({{ site.baseurl }}{% link _posts/2024/03/2024-03-09-stack-overflow-api.html %}),
I began working to keep my promise.
I set up a virtual environment, installed some packages and dug in.
About five code cells later I discovered a missing feature in the software I was using.
I thought that warranted a blog post _before_ my basket analysis post,
so I started to document my journey of logging an issue and submitting a PR.
This required quite a bit of back-and-forth between writing and validating that my notebook and its output would display on my blog correctly.
You could say that having to convert the notebook to HTML, move and rename it to match the expected formatting,
and then copy/paste my front matter to the top of the post was rather annoying 😒.
So annoying that I've decided to write a _pre-pre-post_ covering my solution.
I'll try to be brief.

# Three Steps
The manual process is almost verbatim what I said: convert ➡️ move/rename ➡️ copy/paste ➡️ repeat as necessary ↩️.
Here's a more detailed breakdown.

#### 1. Convert
Converting a `jupyter notebook` to an HTML document isn't really that hard.
Assuming you [`pip` installed `jupyter`](https://jupyter.org/install),
you should have gotten [`nbconvert`](https://nbconvert.readthedocs.io/en/latest/) along with it.
To convert a notebook to HTML you would do the following from a [terminal](https://en.wikipedia.org/wiki/Terminal_emulator)
/[CLI](https://en.wikipedia.org/wiki/Command-line_interface).
> Note, you should do this from the environment where you installed `jupyter` and `nbconvert`.

```shell
jupyter nbconvert --to html path/to/your/notebook.ipynb
```

That's it! You'll now see your original _notebook.ipynb_ as well as a ✨new✨ _notebook.html_.
On to the next step.

#### 2. Move/Rename
There are a couple ways to do this, and I chose the one that uses the CLI.
The command to move and rename a file are the following:
```shell
mv path/to/your/notebook.html path/to/your/_posts/YYYY-MM-DD-notebook.html
```
Easy, right?
Sure, but if you're working on a post over multiple days,
it can get a tad annoying to have to repeatedly change the date (YYYY-MM-DD).
Speaking from experience 😑.

#### 3. Copy/Paste
Last but not least, the front matter.
Honestly,
this is my least favorite part because it required me to store the front matter in a scratch file where I'd copy it,
then open the newly moved YYYY-MM-DD-notebook.html and paste it at the top.
Oh!
And remember that you have to update the date in the front matter too 🙃.

# Automate the Annoying Stuff
Doing those three steps isn't bad a time or two.
But remembering to hit the up-key on my CLI twice to convert the notebook, another two times to move it,
and then the copy/paste nonsense... I'd had enough.

After a bit of toying with a bash script (not my forté 😩), I went with a Python script (definitely my forté 😎).
Here it is with all its glory!

```python
# Contents of ipynb_to_post.py

from pathlib import Path
import subprocess
from typing import Final

import typer


FRONT_MATTER: Final[str] = """---
layout: "post"
title: "{title}"
date: {date}
---

"""


def main(file: str) -> None:
    file_path = Path(file)
    title = file_path.stem.title()
    subprocess.run(
        args=f"jupyter nbconvert --to html {file_path.as_posix()}"
    )
    html = file_path.with_suffix(suffix=".html")
    date = html.parent.name
    mv = html.with_name(name=f"{date}-{html.name}")
    post_path = Path(f"./_posts/{mv.name}")
    subprocess.run(args=f"mv {html.as_posix()} {post_path.as_posix()}")
    with post_path.open(mode="r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f"{FRONT_MATTER.format(title=title, date=date)}{content}")


if __name__ == "__main__":
    typer.run(main)

```

Okay, it isn't the _best_ solution, but it works!
All you do is go to the CLI and run it with the following:

```shell
python ipynb_to_post.py path/to/your/notebook.ipynb
```

And bada bing bada boom, the steps are complete.
No more annoying convert-move-rename-copy-paste stuff.
> Side note, the script should be run from the same level as your \_posts directory.

# Conclusion
There you have it, folks.
A post produced by an annoyance, that came from a post produced by a missing feature, that came from a post with a promise.
I'll refrain from anymore promises until I keep the one I've delayed 😉.

> P.S. here's a link to the
> [_ipynb_to_post.py_](https://github.com/it176131/it176131.github.io/blob/main/ipynb_to_post.py) script.