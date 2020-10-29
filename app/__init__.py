import os

from flask import Flask
from flask import render_template, url_for

app = Flask(__name__)


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

@app.route('/dataaccess/')
def data_access():
    return render_template('dataAccess.html')
if __name__ == '__main__':
    app.run()