from . import app

if __name__ == '__main__':
    app.run()

''''
I thought you just copied the file below, but I keep the contents just in case. (Yuki)

import sys
import pathlib
from .crawler import crawl
from .cleanup import clean

if __name__ == "__main__":
    if len(sys.argv) == 2:
        max_pages = int(sys.argv[1])
    else:
        max_pages = 1000

    # check if parks.json exists and prompt to delete
    parks_json = pathlib.Path("parks.json")
    if parks_json.exists():
        print("parks.json already exists. Rescrape? [y/n]")
        if input().lower() == "y":
            crawl(max_pages)
    else:
        crawl(max_pages)

    print("Cleaning parks.json and writing to normalized_parks.json")
    clean()
'''