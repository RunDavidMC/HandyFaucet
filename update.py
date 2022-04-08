import git
import requests
import os, sys
import time
from threading import Thread

def update(v, repo, res, pref):
    print("Found a new version: " + res.json()["tag_name"] + ".\nYou are currently on " + v + ".")
    print("Changelog: " + res.json()["body"])

    conf = None

    def check():
        time.sleep(10)
        if conf != None:
            return
        print("Falling back to default option (" + pref + ")...")
        conf = pref

    Thread(target = check).start()

    conf = input("Do you want to update to this version (if you do not answer in 10 seconds, the updater will fall back on your default option)? [y/n] ")

    if conf[0].lower() == "y":
        print("Updating...")
        repo.git.pull()
        print("Update complete. Restarting...")
        os.execv(sys.argv[0], sys.argv)
    else:
        print("Aborting...")
        return


def check(repo, v, pref):
    res = requests.get("https://api.github.com/repos/" + repo + "/releases/latest")

    try:
        info = res.json()
        e = info["tag_name"]
        del e
    except:
        print("Could not connect to GitHub to check for updates. Aborting...")
        return

    if info["tag_name"].startswith(v[0]):
        info = info["tag_name"].strip(v[0])
        vr = v
        v = v.strip(v[0])
        info = info.split(".")
        v = v.split(".")

        if info[0] > v[0]:
            update(vr, repo, res, pref)
        elif info[1] > v[1] and info[0] == v[0]:
            update(vr, repo, res, pref)
        elif info[2] > v[2] and info[0] == v[0] and info[1] == v[1]:
            update(vr, repo, res, pref)
        else:
            print("You are up to date.")
            return