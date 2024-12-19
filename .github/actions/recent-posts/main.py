import httpx
from httpx import Response

if __name__ == "__main__":
    BLOG_URL = "https://it176131.github.io/feed.xml"
    resp: Response = httpx.get(url=BLOG_URL)
    xml = resp.content
    print(xml)
