import os

from flask import Flask
from flask import render_template, url_for
from app.forms import DataAccessForm
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def runit():
    with app.open_resource('static/HomeResearchDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('home.html', description=content)

@app.route('/researchteam/')
def research_team():
    return render_template('researchTeam.html')

@app.route('/quasarresearchabout/')
def quasar_research_about():
    with app.open_resource('static/QuasarResearchAboutPageDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('quasarResearchAbout.html', description=content)

@app.route('/dataaccess/', methods = ["GET", "POST"])
def data_access():
    form = DataAccessForm()
    return render_template('dataAccess.html', form=form)

if __name__ == '__main__':
    app.run()