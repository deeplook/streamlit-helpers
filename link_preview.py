# Simplified version of https://www.alanshawn.com/tech/2020/03/25/link-preview.html

from dataclasses import dataclass
from datetime import datetime
from textwrap import dedent
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


CSS = '''\
<style>
.div-link-preview {
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    border: 2px solid #C0C0C0;
    overflow: hidden;
    width: 90%;
    margin-bottom: 10px;
}

.div-link-preview:after {
    content: "";
    display: table;
    clear: both;
}

.div-link-preview-col {
    float: left;
}

.div-link-preview-col-l {
    width: 18%
}

.div-link-preview-col-r {
    width: 80%;
    padding-top: 5px;
}

.div-link-preview-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.div-link-preview-content::-webkit-scrollbar {
    width: 0px;
    background: transparent; /* Chrome/Safari/Webkit */
}

.div-link-preview-title {
    display: block;
    margin-right: auto;
    width: 98%;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #101010;
    text-decoration: underline;
}

.div-link-preview-title a{
    color: #101010;
    text-decoration: underline;
}

.div-link-preview-content {
    display: block;
    font-size: small;
    height: 58%;
    overflow: auto;
    color: #606060;
}

.div-link-preview-domain {
    padding-right: 2%;
    display: block;
    font-weight: bold;
    color: #808080;
    text-align: right;
    font-size: 80%;
    font-family: Arial, Helvetica, sans-serif;
}
</style>
'''


JAVASCRIPT = '''\
<script>
    function adjustLinkPreviewHeight(){
      console.log("running!");
      var cats = document.querySelectorAll(".div-link-preview");
      //console.log(cats.length);
      for (var i = 0; i < cats.length; i++) {
        var left = cats[i].querySelector(".div-link-preview-col-l");
        var right = cats[i].querySelector(".div-link-preview-col-r");
        var width = left.clientWidth;
        cats[i].style.height = width + "px";
        left.style.height = width + "px";
        right.style.height = width + "px";
      }
    }

    adjustLinkPreviewHeight();
</script>
'''


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive"
}


PREVIEW = '''\
<div class="div-link-preview">
    <div class="div-link-preview-col div-link-preview-col-l">
        <img class="div-link-preview-img" src="{result.image}">
    </div>
    <div class="div-link-preview-col div-link-preview-col-r">
        <div style="display: block; height: 100%; padding-left: 10px;">
            <div class="div-link-preview-title"><a href="{result.link}">{result.title}</a></div>
            <div class="div-link-preview-content">{result.description}</div>
            <div class="div-link-preview-domain">
            <span style="font-size: 80%;">&#x1F4C5;</span>&nbsp;{result.access_date}
            <span style="font-size: 80%; margin-left: 20px;">&#x1F517;</span>&nbsp;{result.domain}</div>
        </div>
    </div>
</div>
'''.strip()


@dataclass
class Result:
    link: str
    title: str
    image: str
    domain: str
    description: str
    access_date: str


class LinkPreview:
    def __init__(self, headers=None, preview=None, css=None, javascript=None):
        self.css = css or CSS
        self.headers = headers or HEADERS
        self.preview = preview or PREVIEW
        self.javascript = javascript or JAVASCRIPT

    def resolve_title(self):
        tag = self.soup.find("meta", attrs={"property": "og:title"})
        if tag is not None and "content" in tag.attrs:
            return tag["content"]

        tag = self.soup.find("title")
        if tag is not None:
            return tag.text

    def resolve_image(self):
        soup = self.soup
        urlbase = self.urlbase

        tag = soup.find("meta", attrs={"property": "og:image"})
        if tag is not None and "content" in tag.attrs:
            return urljoin(urlbase, tag["content"])

        tag = soup.find("link", attrs={"rel": "shortcut icon"})
        if tag is not None and "href" in tag.attrs:
            return urljoin(urlbase, tag["href"])

        tag = soup.find("img")
        if tag is not None and "src" in tag.attrs:
            return urljoin(urlbase, tag["src"])

    def resolve_description(self):
        tag = self.soup.find("meta", attrs={"property": "og:description"})
        if tag is not None and "content" in tag.attrs:
            return tag["content"]

        body = self.soup.find("body")
        if body is not None:
            tag = body.find("p")
            if tag is not None:
                return tag.text

    def resolve_domain(self):
        tag = self.soup.find("meta", attrs={"property": "og:url"})
        if tag is not None and "content" in tag.attrs:
            ogurlinfo = urlparse(tag["content"])
            if len(ogurlinfo.netloc) > 0:
                return ogurlinfo.netloc
        return self.urlinfo.netloc

    def process(self, link):
        self.link = link
        self.urlinfo = ui = urlparse(link)
        if len(ui.scheme) == 0 or len(ui.netloc) == 0:
            msg = "Please use complete URL starting with http:// or https:// ."
            raise RuntimeError(msg)
        self.urlbase = f"{ui.scheme}://{ui.netloc}"
        content = requests.get(link, headers=self.headers).content
        self.soup = BeautifulSoup(content, "html5lib")
        self.result = Result(
            link = link,
            title = self.resolve_title(),
            image = self.resolve_image(),
            domain = self.resolve_domain(),
            description = self.resolve_description(),
            access_date = datetime.now().strftime("%Y-%m-%d")
        )

    def make_preview(self):
        return self.preview.format(result=self.result)
