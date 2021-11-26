import argparse
import bs4
import json
import os
import re
import requests

from pathlib import Path

works = {
    "worm": "https://parahumans.wordpress.com/2011/06/11/1-1/",
    "pale": "https://palewebserial.wordpress.com/2020/05/05/blood-run-cold-0-0/",
    "pact": "https://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/",
    "ward": "https://www.parahumans.net/2017/10/21/glow-worm-0-1/"
    }


def quote(s):
    table = str.maketrans('\\/:|', '    ')
    return s.translate(table)


parser = argparse.ArgumentParser()
parser.add_argument('work')
parser.add_argument('-start', nargs=2, default=[0, None])
args = parser.parse_args()

work = args.work
if args.start[1] is None:
    url = works[work]
else:
    url = args.start[1]

if not os.path.exists(work):
    os.mkdir(work)

def punctuation_to_ascii(text):
    table = json.loads(Path(r"symbolTable.json").read_text(encoding='utf-8'))
    table = {int(key): value for key, value in table.items()}
    return text.translate(table).replace('\xa0', ' ') # nbsp

for i in range(int(args.start[0]), 1000):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    title = quote(soup.find("title").text)
    title = title.replace('\n', '').replace('\t', '')
    print(title.encode('866', 'replace').decode('866'))
    text = soup.select_one(".entry-content").get_text()
    text = punctuation_to_ascii(text)
    filename = '{}/{:03d} - {}.txt'.format(work, i, title)
    filename = filename.replace('\n', '')
    filename = filename.replace('\t', '')
    filename = filename.replace('\u2013', '-')
    with open(
            filename,
            'w', encoding='utf8') as f:
        f.write(text)
    next_chapter = soup.find("a", text=re.compile("(?i)Next Chapter"))
    if next_chapter is None:
        next_chapter = soup.find("a", text=re.compile("(?i)ex Chapr"))
    if next_chapter is None:
        break
    url = next_chapter["href"]
