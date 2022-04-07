from flask import Flask, send_file, render_template, request, redirect, url_for, send_from_directory, jsonify
from waitress import serve
import sqlite3
import db

from config import options, info, webserver, webhooks

options = options()
info = info()
webserver = webserver()
webhooks = webhooks()

cnx = sqlite3.connect('main.db')


app = Flask(__name__)

def rt(file, **kwargs):
    return render_template(file, name=options.faucet_name, **kwargs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 
    else:
        return rt('index.html', title='Home')


if __name__ == "__main__":
    serve(app, host=webserver.host, port=webserver.port)