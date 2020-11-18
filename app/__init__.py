import os
import pymysql
import csv

from flask import Flask
from flask import render_template, url_for, g, request, send_file
from app.forms import DataAccessForm
from app.config import Config
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)

def connect_db():
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
        if(form.Download.data):
            #Get the QSO for all checked rows
            downloadItems = request.form.getlist('downloadItem')

            if(downloadItems):
                #turn the checked items into string list for SQL query
                downloadItemsSQLList = "("
                count = 1
                for i in downloadItems:
                    if(count != len(downloadItems)):
                        downloadItemsSQLList = downloadItemsSQLList + "'" + i + "', "
                    else:
                        downloadItemsSQLList = downloadItemsSQLList + "'" + i + "')"
                    count+=1

                sql = "SELECT * FROM quasarinfo WHERE TRIM(QSO) in %s" % (downloadItemsSQLList)
                cursor = get_db().cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql)
                
                rows = cursor.fetchall()

                fp = open('app/tmp/quasars.csv', 'w', newline='')
                myFile = csv.writer(fp)
                myFile.writerow(rows[0].keys())
                for row in rows:
                    myFile.writerow(row.values())
                fp.close()
                try:
                    return send_file('tmp/quasars.csv', attachment_filename='quasars.csv', as_attachment=True)
                except Exception as e:
                    return str(e)

        elif(form.Submit.data):
            cursor = get_db().cursor()

            QSO = form.QSO.data
            MDJ_FIBER = form.Plate_MJD_fiber.data
            ZEMDR9Q_Min = form.ZEMDR9Q_Min.data
            ZEMDR9Q_Max = form.ZEMDR9Q_Max.data
            ZEMHW10_Min = form.ZEMHW10_Min.data
            ZEMHW10_Max = form.ZEMHW10_Max.data
            BALQSO = form.BALQSO.data
            sql= None
            vars = list()

            #Check QSO
            if(len(QSO) > 0):
                sql = "SELECT * FROM quasarinfo WHERE trim(QSO) = %s"
                vars.append(QSO)

            #check MJD_Fiber
            if(MDJ_FIBER):
                if(sql):
                    sql = sql + ' AND trim(PLATE_MJD_FIBER) = %s'
                else:
                    sql ='SELECT * FROM quasarinfo WHERE trim(PLATE_MJD_FIBER) = %s'
                vars.append(MDJ_FIBER)

            #Check ZEMDR9Q
            if(ZEMDR9Q_Min and ZEMDR9Q_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q BETWEEN %s AND %s'
                vars.append(ZEMDR9Q_Min)
                vars.append(ZEMDR9Q_Max)

            elif (ZEMDR9Q_Min):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q >= %s'
                vars.append(ZEMDR9Q_Min)

            elif (ZEMDR9Q_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q <= %s '
                vars.append(ZEMDR9Q_Max)

            #Check ZEMHW10
            if(ZEMHW10_Min and ZEMHW10_Max):
                if(sql):
                    sql = sql + ' AND ZEMHW10 BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMHW10 BETWEEN %s AND %s'
                vars.append(ZEMHW10_Min)
                vars.append(ZEMHW10_Max)

            elif (ZEMHW10_Min):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q >= %s'
                vars.append(ZEMHW10_Min)

            elif (ZEMHW10_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo WHERE ZEMDR9Q <= %s '
                vars.append(ZEMHW10_Max)

            #Check BALQSO
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

        if data:
            return render_template('dataAccess.html', form=form, data=data)

    return render_template('dataAccess.html', form=form)

if __name__ == '__main__':
    app.run()