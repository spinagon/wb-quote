import argparse
import glob
import random
import re

def quote(work):
    names = glob.glob('/home/flak.yar/wb-quote/' + work + '/*.txt')
    quotes = []

    retry = 30
    while (not quotes) and (retry > 0):
        retry -= 1
        try:
            with open(random.choice(names), 'r', encoding='utf-8') as f:
                text = f.read()

            quotes = re.findall("“.*?”", text)
        except Exception as e:
            print(e)
            continue

    q = random.choice(quotes)
    if len(q.split(' ')) < 3:
        return quote(work)
    return q


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('work')
    args = parser.parse_args()

    work = args.work

    q = quote(work)

    q = q.replace('\xa0', ' ')
    q = q.replace('\u201c', '"')
    q = q.replace('\u201d', '"')
    q = q.replace('\u2019', "'")
    q = q.replace('\u2026', "...")

    try:
        print(q)
    except Exception:
        print(q.encode('866', 'xmlcharrefreplace'))
