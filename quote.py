# coding: utf-8

import argparse
import glob
import random
import re
import os


def quote(work):
    basedir = '/home/flak.yar/wb-quote/'
    if not os.path.exists(basedir):
        basedir = r'c:/Documents and Settings/hramatograf/Мои документы/py/wb-quote/'
    names = glob.glob(basedir + work + '/*.txt')
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

    i = random.choice(range(len(quotes)))
    # Backtrack to first sentence ending with comma
    while i > 0 and quotes[i - 1][-2] == ',':
        i -= 1
    q = quotes[i]
    i += 1
    # Go forward until sentence doesn't end with comma
    while q[-2] == ',' and i < len(quotes):
        q += '\n' + quotes[i]
        i += 1
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
    q = q.replace('\u2018', "'")

    try:
        print(q)
    except Exception:
        print(q.encode('866', 'xmlcharrefreplace').decode('utf8'))
