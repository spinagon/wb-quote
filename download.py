import requests
import bs4
import re
import os
import argparse

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
args = parser.parse_args()

work = args.work
url = works[work]

if not os.path.exists(work):
    os.mkdir(work)

for i in range(1000):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    title = quote(soup.find("title").text)
    title = title.replace('\n', '').replace('\t', '')
    print(title.encode('866', 'replace').decode('866'))
    text = soup.select_one(".entry-content").get_text()
    with open(
            '{}/{:03d} - {}.txt'.format(work, i, title),
            'w', encoding='utf8') as f:
        f.write(text)
    next_chapter = soup.find("a", text=re.compile("(?i)Next Chapter"))
    if next_chapter is None:
        next_chapter = soup.find("a", text=re.compile("(?i)ex Chapr"))
    if next_chapter is None:
        break
    url = next_chapter["href"]
