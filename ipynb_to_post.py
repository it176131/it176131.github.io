# https://stackoverflow.com/questions/89228/how-do-i-execute-a-program-or-call-a-system-command

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

COMMENTS: Final[str] = """
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
</script>"""


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
    with post_path.open(mode="r+", encoding="utf-8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(
            f"{FRONT_MATTER.format(title=title, date=date)}{content}{COMMENTS}"
        )


if __name__ == "__main__":
    typer.run(main)
