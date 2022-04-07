from cgi import test
from flask import Flask, send_file, render_template, request, redirect, url_for, send_from_directory, jsonify, flash, session, abort
from waitress import serve
import sqlite3
import requests

import db

from config import options, info, webserver, webhooks

### DECLARE VARIABLES ###

options = options()
info = info()
webserver = webserver()
webhooks = webhooks()

cookies = {"namebase-main": info.nb_cookie}
nb_endpoint = "https://www.namebase.io/"

### ----------------- ###

cnx = sqlite3.connect('main.db')

db.verify(cnx)

cxt = cnx.cursor()

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

def rt(file, **kwargs):
    return render_template(file, name=options.faucet_name, **kwargs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_verify = cxt.execute("SELECT * FROM claims WHERE email=?", (request.form['email'])).fetchall()
        if len(email_verify) != 0:
            return rt("index.html", title='Home', error="Email has already been used.")

        ip_verify = cxt.execute("SELECT * FROM claims WHERE ip=?", (request.remote_addr)).fetchall()
        if len(ip_verify) != 0:
            return rt("index.html", title='Home', error="IP has already been used.")

        
    else:
        return rt('index.html', title="Home")


if __name__ == "__main__":
    serve(app, host=webserver.host, port=webserver.port)