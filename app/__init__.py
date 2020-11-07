import os
import pymysql

from flask import Flask
from flask import render_template, url_for, g, request
from app.forms import DataAccessForm
from app.config import Config



app = Flask(__name__)
app.config.from_object(Config)

def connect_db():
    pwd = os.environ.get('MYSQL_DATABASE_PASSWORD')
    print("PSWD is: " + pwd)
    return pymysql.connect(
        host = 'localhost', user = 'root', password = os.environ.get('MYSQL_DATABASE_PASSWORD'),
        database = 'test', autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor) 

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


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
    form = DataAccessForm(request.form)
    data = None
    if request.method == "POST":
        if form.is_submitted():
            print("Form successfully submitted")
        cursor = get_db().cursor()

        QSO = form.QSO.data
        ZEMDR9Q_Min = form.ZEMDR9Q_Min.data
        print(ZEMDR9Q_Min)
        ZEMDR9Q_Max = form.ZEMDR9Q_Max.data
        BALQSO = form.BALQSO.data

        sql= None
        vars = list()

        if(len(QSO) > 0):
            sql = "SELECT * FROM quasarinfo WHERE trim(QSO) = %s"
            vars.append(QS0)

        if(ZEMDR9Q_Min and ZEMDR9Q_Max):
            if(sql):
                sql = sql + ' AND ZEMDR9Q BETWEEN %s AND %s'  % (str(ZEMDR9Q_Min), str(ZEMDR9Q_Max))
            else:
                sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q BETWEEN %s AND %s' % (str(ZEMDR9Q_Min), str(ZEMDR9Q_Max))

        elif (ZEMDR9Q_Min):
            if(sql):
                 sql = sql + ' AND ZEMDR9Q >= %s'
            else:
                sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q >= %s '

        elif (ZEMDR9Q_Max):
            if(sql):
                 sql = sql + ' AND ZEMDR9Q <= %s'
            else:
                sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q <= %s '
        
        if (len(BALQSO) > 0):
            if(sql):
                 sql = sql + " AND trim(BALQSO) = %s"
            else:
                sql = "SELECT * FROM quasarinfo WHERE trim(BALQSO) = %s"
            vars.append(BALQSO)

        if(sql):
            cursor = get_db().cursor()
            print(sql)
            cursor.execute(sql, tuple(vars))
            data = cursor.fetchall()
            print(data)

    if data:
        return render_template('dataAccess.html', form=form, data=data)

    return render_template('dataAccess.html', form=form)

if __name__ == '__main__':
    app.run()