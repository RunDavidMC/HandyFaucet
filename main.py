from flask import Flask, send_file, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session, abort
from waitress import serve
import sqlite3
import requests
import json
import time
import sys
import os

import db
import update

from config import options, info, encryption, webserver, admin, webhooks

### DO NOT CHANGE ###

v = "v0.0.5"
repo = "RunDavidMC/HandyFaucet"

### DO NOT CHANGE ###

upd = update.check(repo, v)

### DECLARE VARIABLES ###

options = options()
encryption = encryption()
info = info()
webserver = webserver()
admin = admin()
webhooks = webhooks()

cookies = {"namebase-main": info.nb_cookie}
nb_endpoint = "https://www.namebase.io/"

### ----------------- ###

cnx = sqlite3.connect('main.db', check_same_thread=False)
cxt = cnx.cursor()

db.verify(cxt)

print("Successfully connected to database.")

conn_test = requests.get(nb_endpoint + "api/user", cookies=cookies)
try:
    nb_referral = conn_test.json()["referralCode"]
    print("Successfully connected to Namebase.")
    del conn_test
except:
    print("Could not connect to Namebase. Make sure your cookie is correct.")
    exit()

app = Flask(__name__)

app.url_map.strict_slashes = False
app.secret_key = encryption.session_key

def rt(file, **kwargs):
    return render_template(file, faucet_name=info.faucet_name, **kwargs)

def get_nb_names():
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    url = nb_endpoint + "/api/user/domains/not-listed/0?sortKey=acquiredAt&sortDirection=desc&limit=100"
    totalCount = requests.get(url, timeout=30, cookies=cookies).json()['totalCount']
    domains = []
    offset = 0
            
    while totalCount > 0:
        totalCount -= 100
        url = nb_endpoint + "/api/user/domains/not-listed/" + str(offset) + "?sortKey=acquiredAt&sortDirection=desc&limit=100"
        res = requests.get(url, timeout=10, cookies=cookies).json()['domains']
        for x in res:
            res2 = x['name']
            [domains.append(res2)]
        offset += 100

    return domains

if options.lazy_load_domains:
    print("Loading domains from Namebase...")
    nb_domains = get_nb_names()
    

print(info.faucet_name + " is now running.")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_verify = cxt.execute("SELECT * FROM claims WHERE email=?", [request.form['email']]).fetchall()
        if len(email_verify) != 0:
            return rt("index.html", title='Home', error="Email has already been used.")

        ip_verify = cxt.execute("SELECT * FROM claims WHERE ip=?", [request.remote_addr]).fetchall()
        if len(ip_verify) != 0:
            return rt("index.html", title='Home', error="IP has already been used.")

        name = cxt.execute("SELECT * FROM names ORDER BY RANDOM() LIMIT 1;").fetchone()

        if name == None:
            if webhooks.notify_out_of_names:
                requests.post(webhooks.out_of_names_url, data={"content": webhooks.out_of_names_message, "username": info.faucet_name})
            return rt("index.html", title='Home', error="No names left.")
        
        name = name[0].strip(",")

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        params = {"recipientEmail": request.form['email'], "senderName": info.faucet_name,
                  "note": "Built by RunDavidMC"}

        send_name = requests.post(nb_endpoint + "/api/gift/" + name.strip("\n"), headers=headers,
                          data=json.dumps(params), cookies=cookies)

        if send_name.status_code != 200:
            if webhooks.notify_name_send_error:
                requests.post(webhooks.name_send_error_url, json={"content": webhooks.name_send_error_message + " | ERROR: " + str(send_name.json()), "username": info.faucet_name})
            return rt("index.html", title='Home', error="Could not send name.")

        cxt.execute("INSERT INTO claims (name, email, ip, time) VALUES (?, ?, ?, ?)", [name, request.form['email'], request.remote_addr, int(time.time())])
        cxt.execute("DELETE FROM names WHERE name=?", [name])
        cnx.commit()

        return rt("success.html", title='Success', name=name, email=request.form['email'], connections=info.connections)

    else:
        return rt('index.html', title="Home")

@app.route("/" + admin.path, methods=['GET', 'POST'])
def adminPanel():
    if request.method == 'POST':
        if 'admin' not in session:
            if request.form['password'] == admin.password:
                session['admin'] = True
                return rt('adminDash.html', title='Admin Panel')
            else:
                return rt('adminLogin.html', title='Admin Login', error="Incorrect password.")
        else:
            if int(request.form['pin']) != int(admin.pin):
                return rt('adminDash.html', title='Admin Panel', error="Incorrect PIN!")

            names = request.form['names']
            names = names.split("\n")
            names2 = []
            for name in names:
                if name.strip("\r").strip("/") != "":
                    names2.append(name.strip("\r").strip("/"))
            names = names2
            names = list(dict.fromkeys(names))

            names_confirmed = []

            if options.lazy_load_domains:
                domains = nb_domains
            else:
                domains = get_nb_names()

            for dom in domains:
                if dom in names:
                    names.remove(dom)
                    names_confirmed.append(dom)

            if len(names_confirmed) > 0:
                for x in names_confirmed:
                    try:
                        cxt.execute("INSERT INTO names (name) VALUES (?)", [x])
                    except:
                        pass
                cnx.commit()
                success = "Successfully loaded " + str(len(names_confirmed)) + " names."
            else:
                success = None

            if len(names) > 0:
                error = "Could not load: "
                for x in names:
                    error += x + "/, "
            else:
                error = None

            return rt('adminDash.html', title='Admin Panel', error=error, success=success)

    else:
        if 'admin' in session:
            return rt('adminDash.html', title='Admin Panel')
        else:
            return rt('adminLogin.html', title='Admin Login')


if __name__ == "__main__":
    serve(app, host=webserver.host, port=webserver.port)
