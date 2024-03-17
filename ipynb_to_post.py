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
