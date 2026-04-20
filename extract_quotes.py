# coding: utf-8

import argparse
import glob
import os
import re
import json


def extract(work):
    basedir = "/home/flak.yar/wb-quote/"
    if not os.path.exists(basedir):
        basedir = r"/mnt/d/wb-quote/"
    names = glob.glob(basedir + work + "/*.txt")
    quotes = []

    for name in names:
        try:
            with open(name, "r", encoding="utf-8") as f:
                text = f.read()
            quotes.append({"chapter": name, "quotes": re.findall('["“].*?["”]', text)})
        except Exception as e:
            print(e)
            continue

    coalesced_quotes = [
        {"chapter": quotes[0]["chapter"], "quote": quotes[0]["quotes"][0]}
    ]
    for x in quotes:
        match = re.search(r"(\d{3}\s-\s)(.*)\s+(\w+)\.txt", x["chapter"])
        work_name = match.group(3)
        chapter = match.group(2)
        source = f"{work_name} - {chapter}"
        q_list = x["quotes"]
        if not q_list:
            continue
        for q in q_list:
            if coalesced_quotes[-1]["quote"][-2] == ",":
                coalesced_quotes[-1]["quote"] += f"<br>{q}"
            else:
                coalesced_quotes[-1]["quote"] += f"<br>{source}"
                coalesced_quotes.append({"chapter": chapter, "quote": q})

    with open(f"{work}_quotes.json", "w") as f:
        json.dump(coalesced_quotes, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("work")
    args = parser.parse_args()

    work = args.work

    extract(work)
