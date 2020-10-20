import os

from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)


@app.route('/')
def runit():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()