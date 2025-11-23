from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


async def fetch_metadata_from_url(url: str):
    # Validate URL
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        return {"error": "Invalid URL"}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to retrieve page, status code: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else None

    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"].strip() if meta_description else None

    # Get base URL for resolving relative paths
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    # Fallback chain for favicon
    icon_link = soup.find("link", rel=["icon", "shortcut icon"])
    if icon_link:
        favicon = urljoin(base_url, icon_link["href"])
    else:
        favicon = urljoin(base_url, "/favicon.ico")

    return {"url": url, "title": title, "description": description, "favicon": favicon}
