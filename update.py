import git
import requests
import os, sys
import time
from threading import Thread

def update(v, res):
    print("Found a new version: " + res.json()["tag_name"] + ".\nYou are currently on " + v + ".")
    print("Changelog: " + res.json()["body"])

    conf = input("Do you want to update to this version? [y/n] ")

    if conf[0].lower() == "y":
        print("Updating...")
        g = git.cmd.Git(".")
        g.fetch()
        g.stash("save")
        g.merge()
        g.stash("apply")
        print("Update complete. Please restart.")
        exit()
    else:
        print("Aborting...")
        return


def check(repo, v):
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
            update(vr, res)
        elif info[1] > v[1] and info[0] == v[0]:
            update(vr, res)
        elif info[2] > v[2] and info[0] == v[0] and info[1] == v[1]:
            update(vr, res)
        else:
            print("You are up to date.")
            return