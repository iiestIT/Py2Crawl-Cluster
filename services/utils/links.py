from Py2Crawl.parser.parser import HTMLParser
from Py2Crawl.settings import ParserSettings
from urllib.parse import urlparse


class LinkParser:
    def __init__(self, html: str, start_url: str):
        self.extensions = ParserSettings.skip_extensions + [".js", ".jsx", ".css", ".json"]
        self.skip_chars = [
        ")", "(", "[", "]", "{", "}", "\\", "+", "*", "'", "\"", "<", ">", "|", "@", "€", "!", "§", "$", "%", "&", "=",
        "?", "#", "~"
        ]
        self.html = html
        self.start_url = start_url

    async def links(self):
        parser = HTMLParser(self.html)
        _nl = await parser.get_all_links_from_scope(self.start_url)
        link_list: list = await parser.get_all_links()
        link_list = list(map(self._format_link, link_list))
        next_link = list(set(map(self._format_link, filter(self._parser_next_links, _nl))))
        return link_list, next_link

    def _parser_next_links(self, url: str):
        if urlparse(url).netloc == "" \
                and not any(filter(lambda x: url.startswith(str(x)), self.skip_chars)) \
                and not any(filter(lambda x: x in url, self.extensions)):
            return True
        elif not urlparse(url).netloc == "" and any(
                filter(lambda x: x in url, self.extensions)) == False:
            return True
        else:
            return False

    def _format_link(self, url: str):
        if urlparse(url).netloc == "":
            if ".." in url:
                url = url.replace("..", "")
            if not url.startswith("/"):
                n_url = f"https://{urlparse(self.start_url).netloc}/{url}"
            else:
                n_url = f"https://{urlparse(self.start_url).netloc}{url}"
            if "#" in n_url:
                return n_url.split("#")[0]
            if "?" in n_url:
                return n_url.split("?")[0]
            return n_url
        else:
            if "#" in url:
                return url.split("#")[0]
            if "?" in url:
                return url.split("?")[0]
            return url