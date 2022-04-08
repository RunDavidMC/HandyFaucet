import requests
import urllib'
import os

def update(v, info, repo):
    path = os.path.dirname(__file__)

    confirm = input("Found a new version: " + info + "\n You are currently on " + v + "\n Would you like to update [y/n]? ")

    if confirm.lower() != "y":
        print("Not updating.")
        return

    with urllib.request.urlopen("https://api.github.com/repos/" + repo + "/zipball/" + info) as upd:
        with open(path, "wb+") as file:
            file.write(upd.read())



def check(repo, v, auto_update):
    info = requests.get("https://api.github.com/repos/" + repo + "/releases/latest")
    
    try:
        info = info.json()
    except:
        print("Could not check for updates.")
        return

    if info["tag_name"].startswith(v[0]):
        info = info["tag_name"].strip(v[0])
        v = v.strip(v[0])
        info = info.split(".")
        v = v.split(".")

        if info[0] > v[0]:
            update(v, info, repo)
        elif info[1] > v[1] and info[0] == v[0]:
            update(v, info, repo)
        elif info[2] > v[2] and info[0] == v[0] and info[1] == v[1]:
            update(v, info, repo)

