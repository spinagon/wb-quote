# coding: utf-8

import argparse
import os
import random
import json


def quote(work):
    basedir = "/home/flak.yar/wb-quote/"
    if not os.path.exists(basedir):
        basedir = r"c:/Documents and Settings/hramatograf/Мои документы/py/wb-quote/"

    with open(f"{work}_quotes.json", "r") as f:
        quotes = json.load(f)

    q = random.choice(quotes)
    return q["quote"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("work")
    args = parser.parse_args()

    work = args.work

    q = quote(work)

    q = q.replace("\xa0", " ")
    q = q.replace("\u201c", '"')
    q = q.replace("\u201d", '"')
    q = q.replace("\u2019", "'")
    q = q.replace("\u2026", "...")
    q = q.replace("\u2018", "'")
    q = q.replace("<br>", "\n")

    try:
        print(q)
    except Exception:
        print(q.encode("866", "xmlcharrefreplace").decode("utf8"))
