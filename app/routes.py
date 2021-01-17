from flask import Flask
from flask import render_template, url_for, g, request, send_file
from app import app
from app.forms import DataAccessForm
from app.forms import LoginForm
from dotenv import load_dotenv

#Home page
@app.route('/')
def runit():
    with app.open_resource('static/descriptionText/HomeResearchDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('home.html', description=content)

#Login Page
@app.route('/login/')
def login():
    form = LoginForm(request.form)
    return render_template('login.html', title='Sign In', form=form)

#Team page
@app.route('/researchteam/')
def research_team():
    try:
        with app.open_resource('static/descriptionText/teamMembersDescriptions/paolaDescription.txt') as f:
            paolaContent = f.read().decode('utf-8')
    except Exception as e:
        print(e)
    return render_template('researchTeam.html', paolaDescription = paolaContent)

#Research About/description page
@app.route('/quasarresearchabout/')
def quasar_research_about():
    with app.open_resource('static/descriptionText/QuasarResearchAboutPageDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('quasarResearchAbout.html', description=content)