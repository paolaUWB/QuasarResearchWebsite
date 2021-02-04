import os
import pymysql
import csv
import sys

from flask import Flask
from flask import render_template, url_for, g, request, send_file, flash, redirect
from dotenv import load_dotenv
from functools import wraps

from app.forms import DataAccessForm
from app.config import APP_TMP
from app.config import Config

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

port = os.environ.get('MYSQL_DATABASE_PORT')

# DATABASE METHODS

# Connects to the database
# If won't connect properly to MYSQL, change the port number to match yours
def connect_db():
    port = os.environ.get('MYSQL_DATABASE_PORT')
    # Remote mysql server
    if(port):
        print("world")
        return pymysql.connect(
            host='vergil.u.washington.edu', user='root', password=os.environ.get('MYSQL_DATABASE_PASSWORD'),
            database='quasarWebsite_db', autocommit=True, charset='utf8mb4', port=32445,
            cursorclass=pymysql.cursors.DictCursor)
    # local mysql server
    else:
        print("hello")
        return pymysql.connect(
            host='localhost', user='root', password=os.environ.get('MYSQL_DATABASE_PASSWORD'),
            database='test', autocommit=True, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# Gets the database
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

# Closes the database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


# AUTHENTICATION METHODS

# Requires authentication
# Use for selecting which pages get to be authenticated
def require_login(func):
    @wraps(func)
    def redirect_to_login(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return func()

    return redirect_to_login

# WEBSITE PAGE ROUTES

# Home page route
@app.route('/')
def runit():
    with app.open_resource('static/descriptionText/HomeResearchDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('home.html', description=content)

# Login Page route
# want it to redirect to shibboleth
@app.route('/login/', methods=['GET', 'POST'])
def login():
    return

# Team page route
@app.route('/researchteam/')
def research_team():
    try:
        # Loads descriptions for the professors
        # Paola
        with app.open_resource('static/descriptionText/teamMembersDescriptions/paolaDescription.txt') as f:
            paolaContent = f.read().decode('utf-8')
        # Retik
        with app.open_resource('static/descriptionText/teamMembersDescriptions/retikDescription.txt') as f:
            retikContent = f.read().decode('utf-8')

        # Loads descriptions for the Students
        # Can
        with app.open_resource('static/descriptionText/teamMembersDescriptions/canDescription.txt') as f:
            canContent = f.read().decode('utf-8')
        # Daria
        with app.open_resource('static/descriptionText/teamMembersDescriptions/dariaDescription.txt') as f:
            dariaContent = f.read().decode('utf-8')
        # Kathleen
        with app.open_resource('static/descriptionText/teamMembersDescriptions/kathleenDescription.txt') as f:
            kathleenContent = f.read().decode('utf-8')
        # Audrey
        with app.open_resource('static/descriptionText/teamMembersDescriptions/audreyDescription.txt') as f:
            audreyContent = f.read().decode('utf-8')
        # Wendy
        with app.open_resource('static/descriptionText/teamMembersDescriptions/wendyDescription.txt') as f:
            wendyContent = f.read().decode('utf-8')
        # Mikel
        with app.open_resource('static/descriptionText/teamMembersDescriptions/mikelDescription.txt') as f:
            mikelContent = f.read().decode('utf-8')
        # David
        with app.open_resource('static/descriptionText/teamMembersDescriptions/davidDescription.txt') as f:
            davidContent = f.read().decode('utf-8')
    except Exception as e:
        print(e)
    return render_template('researchTeam.html', paolaDescription=paolaContent, retikDescription=retikContent,
                           canDescription=canContent, dariaDescription=dariaContent, kathleenDescription=kathleenContent,
                           audreyDescription=audreyContent, wendyDescription=wendyContent, mikelDescription=mikelContent,
                           davidDescription=davidContent,)

# Research about/description page route
@app.route('/quasarresearchabout/')
def quasar_research_about():
    with app.open_resource('static/descriptionText/QuasarResearchAboutPageDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('quasarResearchAbout.html', description=content)

# Data access page route
@app.route('/dataaccess/', methods=["GET", "POST"])
def data_access():
    form = DataAccessForm(request.form)
    data = None
    sql = None

    with app.open_resource('static/descriptionText/DataAccessDescription.txt') as f:
        content = f.read().decode('utf-8')

    if request.method == "POST":
        if(form.Download.data):
            # Get the QSO for all checked rows
            downloadItems = request.form.getlist('downloadItem')

            if(downloadItems):
                # turn the checked items into string list for SQL query
                downloadItemsSQLList = "("
                count = 1
                for i in downloadItems:
                    if(count != len(downloadItems)):
                        downloadItemsSQLList = downloadItemsSQLList + "'" + i + "', "
                    else:
                        downloadItemsSQLList = downloadItemsSQLList + "'" + i + "')"
                    count += 1

                sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE TRIM(t1.QSO) in %s" % (
                    downloadItemsSQLList)
                cursor = get_db().cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql)
                rows = cursor.fetchall()
                try:
                    fp = open(os.path.join(APP_TMP, 'quasars.csv'),
                              'w', newline='')
                except Exception as e:
                    return str(e)

                myFile = csv.writer(fp)
                myFile.writerow(rows[0].keys())
                for row in rows:
                    myFile.writerow(row.values())
                fp.close()
                try:
                    return send_file(os.path.join(APP_TMP, 'quasars.csv'), attachment_filename='quasars.csv', as_attachment=True)
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

            BI_EHVO_min = form.BI_EHVO_min.data
            BI_EHVO_max = form.BI_EHVO_max.data
            V_MAX = form.V_max.data
            V_MIN = form.V_min.data
            EW_min = form.EW_min.data
            EW_max = form.EW_max.data

            sql = None
            vars = list()

            # Check QSO
            # select * from quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t1.QSO) ='J231227.48+005231.7';
            if(len(QSO) > 0):
                sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t1.QSO) = %s"
                vars.append(QSO)

            # check MJD_Fiber
            if(MDJ_FIBER):
                if(sql):
                    sql = sql + ' AND trim(PLATE_MJD_FIBER) = %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t1.PLATE_MJD_FIBER) = %s'
                vars.append(MDJ_FIBER)

            # Check ZEMDR9Q
            if(ZEMDR9Q_Min and ZEMDR9Q_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMDR9Q BETWEEN %s AND %s'
                vars.append(ZEMDR9Q_Min)
                vars.append(ZEMDR9Q_Max)

            elif (ZEMDR9Q_Min):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMDR9Q >= %s'
                vars.append(ZEMDR9Q_Min)

            elif (ZEMDR9Q_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMDR9Q <= %s '
                vars.append(ZEMDR9Q_Max)

            # Check ZEMHW10
            if(ZEMHW10_Min and ZEMHW10_Max):
                if(sql):
                    sql = sql + ' AND ZEMHW10 BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMHW10 BETWEEN %s AND %s'
                vars.append(ZEMHW10_Min)
                vars.append(ZEMHW10_Max)

            elif (ZEMHW10_Min):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMDR9Q >= %s'
                vars.append(ZEMHW10_Min)

            elif (ZEMHW10_Max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.ZEMDR9Q <= %s '
                vars.append(ZEMHW10_Max)

            # Check BALQSO
            if (BALQSO):
                if(sql):
                    sql = sql + " AND trim(BALQSO) = %s"
                else:
                    sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t1.BALQSO) = %s"
                vars.append(BALQSO)

            # Check BI_EHVO
            if(BI_EHVO_min and BI_EHVO_max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.BI_EHVO BETWEEN %s AND %s'
                vars.append(BI_EHVO_min)
                vars.append(BI_EHVO_max)

            elif (BI_EHVO_min):
                if(sql):
                    sql = sql + ' AND BI_EHVO >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.BI_EHVO >= %s'
                vars.append(BI_EHVO_min)

            elif (BI_EHVO_max):
                if(sql):
                    sql = sql + ' AND BI_EHVO <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.BI_EHVO <= %s '
                vars.append(BI_EHVO_max)

            # Check V_Max
            if(V_MAX):
                if(sql):
                    sql = sql + " AND trim(t2.V_MAX) >= %s"
                else:
                    sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t2.V_MAX) >= %s"
                vars.append(V_MAX)

            # Check V_min
            if(V_MIN):
                if(sql):
                    sql = sql + " AND trim(t2.V_MIN) <= %s"
                else:
                    sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE trim(t2.V_MIN) <= %s"
                vars.append(V_MIN)

            # Check EW
            if(EW_min and EW_max):
                if(sql):
                    sql = sql + ' AND ZEMDR9Q BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.EW BETWEEN %s AND %s'
                vars.append(EW_min)
                vars.append(EW_max)

            elif (EW_min):
                if(sql):
                    sql = sql + ' AND EW >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.EW >= %s'
                vars.append(EW_min)

            elif (EW_max):
                if(sql):
                    sql = sql + ' AND EW <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t2.EW <= %s '
                vars.append(BI_EHVO_max)
    if(sql):
        cursor = get_db().cursor()
        cursor.execute(sql, tuple(vars))
        data = cursor.fetchall()
    else:
        sql = "SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO"
        cursor = get_db().cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

    if data:
        return render_template('dataAccess.html', form=form, data=data, description=content)

    return render_template('dataAccess.html', form=form, description=content)

# Test page route
@app.route('/test/')
@require_login
def test():
    return render_template('test.html', title='Test page')


# Runs the app
if __name__ == '__main__':
    app.debug = True
    app.run()
