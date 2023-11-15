#!/bin/python3
from sys import stdout
from git import Repo
import jinja2
import shutil
import os
from pathlib import Path
if not os.path.isdir("bible"):
    Repo.clone_from("https://github.com/piotrskurzynski/biblia.git", "bible")

book_names_repo = []

with open("book_names_repo.txt") as file:
    book_names_repo = [line.rstrip() for line in file]

book_names_pol = []

with open("book_names_pol.txt") as file:
    book_names_pol = [line.rstrip() for line in file]

book_names_path = []

with open("book_names_path.txt") as file:
    book_names_path = [line.rstrip() for line in file]

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
chaptert = env.get_template("chapter.html")
bookst = env.get_template("books.html")

order = []

def chexist(b, ch):
    if os.path.exists("bible/1879/" + b + "/" + ch + ".txt"):
        return True
    if os.path.exists("bible/1879/" + b + "/0" + ch + ".txt"):
        return True
    if os.path.exists("bible/1879/" + b + "/00" + ch + ".txt"):
        return True
    return False

def offch(b, ch, offset):
    return order[(order.index((book_names_path[b] + "/" + str(ch))) + offset) % len(order)]

for i in range(0, len(book_names_repo)):
    j = 1
    while (chexist(book_names_repo[i], str(j))):
        order.append(book_names_path[i] + "/" + str(j))
        j += 1

print(offch(0, 1, -1))

print(len(order))
print(len(order) % len(order))

shutil.rmtree("build")
os.mkdir("build")
for bookf in os.scandir("bible/1879"):
    bookp = "build/" + book_names_path[book_names_repo.index(bookf.name)]
    if not os.path.isdir(bookp):
        os.mkdir(bookp)
    for chapf in os.scandir(bookf.path):
        path = Path(chapf.path)
        verses = []
        with open(path) as file:
            verses = [line.rstrip() for line in file]

        chapter = int(path.name.split(".")[0])

        chapters = [ int(f.name.split(".")[0]) for f in os.scandir(path.parent) ]
        chapters.sort()

        book = book_names_pol[book_names_repo.index(path.parent.name)]

        content = chaptert.render(
            chapter = {"name": str(chapter), "link": "."},
            book = { "name": book, "link": ".." },
            chapters = list(map(lambda e: {"name": str(e), "link": "./" + str(e) + ".html"},chapters)),
            verses = verses,
            next_link = "../" + offch(book_names_repo.index(path.parent.name), chapter, 1) + ".html",
            previous_link = "../" + offch(book_names_repo.index(path.parent.name), chapter, -1) + ".html"
        )

        with open("build/" + book_names_path[book_names_repo.index(bookf.name)] + "/" + str(int(chapf.name.split(".")[0])) + ".html", mode="w", encoding="utf-8") as msg:
            msg.write(content)
    shutil.copy(bookp + "/1.html", bookp + "/index.html")

content = bookst.render(
        books = [{ "name": book_names_pol[i], "link": book_names_path[i]} for i in range(0, len(book_names_repo))]
        )

with open("build/index.html", mode="w", encoding="utf-8") as msg:
    msg.write(content)

shutil.copy("github-mark-white.svg", "build/github-mark-white.svg")

import subprocess
subprocess.run(['npx', 'tailwindcss', '-i', 'main.css', '-o', 'build/main.css'], stdout=stdout)
