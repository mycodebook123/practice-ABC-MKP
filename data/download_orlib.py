import os
import urllib.request

BASE = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/"
FILES = ["mknap1.txt", "mknapcb1.txt", "mknapcb2.txt", "mknapcb3.txt", "mkcbres.txt"]


def download_all(folder=os.path.join("data", "raw")):
    os.makedirs(folder, exist_ok=True)
    for name in FILES:
        target = os.path.join(folder, name)
        if os.path.exists(target):
            print("already there:", name)
            continue
        print("downloading", name)
        urllib.request.urlretrieve(BASE + name, target)


if __name__ == "__main__":
    download_all()