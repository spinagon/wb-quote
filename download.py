# /// script
# name = "Wildbow Scraper"
# version = "0.1.0"
# description = "A simple script to scrape web serial chapters using 'Next Chapter' links."
# dependencies = [
#     "requests",
#     "beautifulsoup4",
#     "lxml",
# ]
# requires-python = ">=3.8"
# ///
import argparse
import json
import os
import re
import time
from pathlib import Path

import bs4
import requests

works = {
    "worm": "https://parahumans.wordpress.com/2011/06/11/1-1/",
    "pale": "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/",
    "pact": "https://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/",
    "ward": "https://www.parahumans.net/2017/10/21/glow-worm-0-1/",
    "twig": "https://twigserial.wordpress.com/category/story/arc-1-taking-root/1-01/",
    "claw": "https://clawwebserial.blog/2024/03/09/the-point-1-1/",
    "seek": "https://seekwebserial.wordpress.com/2024/10/18/0-1-0-hack/",
}


def quote(s):
    table = str.maketrans("\\/:|", "    ")
    return s.translate(table)


parser = argparse.ArgumentParser()
parser.add_argument("work")
parser.add_argument("-start", nargs=2, default=[0, None])
args = parser.parse_args()

work = args.work
if args.start[1] is None:
    url = works[work]
else:
    url = args.start[1]

base_url = re.match("http.*//[^/]+", url).group(0)

if not os.path.exists(work):
    os.mkdir(work)


def punctuation_to_ascii(text):
    return text
    table = json.loads(Path(r"symbolTable.json").read_text(encoding="utf-8"))
    table = {int(key): value for key, value in table.items()}
    return text.translate(table).replace("\xa0", " ")  # nbsp


for i in range(int(args.start[0]), 1000):
    for j in range(5):
        try:
            time.sleep(0.2)
            page = requests.get(url, timeout=10)
            page.encoding = "utf-8"
            soup = bs4.BeautifulSoup(page.text, "lxml")
            title = quote(soup.find("title").text)
            title = title.replace("\n", "").replace("\t", "")
            if title.startswith("Redirecting"):
                url = soup.find("a")["href"]
                continue
            break
        except Exception as e:
            print(repr(e))
            continue

    print(title.encode("866", "replace").decode("866"))
    print(url)
    text = soup.select_one(".entry-content").get_text()
    text_html = str(soup.select_one("article"))
    text = punctuation_to_ascii(text)
    text_html = punctuation_to_ascii(text_html)

    filename = "{}/{:03d} - {}.html".format(work, i, title)
    filename = filename.replace("\n", "")
    filename = filename.replace("\t", "")
    filename = filename.replace("\u2013", "-")
    with open(filename, "w", encoding="utf8") as f:
        f.write(text_html)

    filename = "{}/{:03d} - {}.txt".format(work, i, title)
    filename = filename.replace("\n", "")
    filename = filename.replace("\t", "")
    filename = filename.replace("\u2013", "-")
    with open(filename, "w", encoding="utf8") as f:
        f.write(text)

    next_chapter = soup.find("a", string=re.compile("(?i)Next Chapter"))
    if next_chapter is None:
        next_chapter = soup.find("a", string=re.compile("(?i)ex Chapr"))
    if next_chapter is None:
        next_chapter = soup.find("a", rel="next")
    if next_chapter is None:
        next_chapter = soup.find("a", string=re.compile("(?i)Next"))
    if next_chapter is None:
        break
    url = next_chapter["href"]
    if url[0] == "/":
        url = base_url + url
