# TITLE: Routes
# CONTRIBUTORS: Kathleen Guinee, Audrey Nguyen
# DESCRIPTION: Contains the website routes

import pymysql
import os
import csv

from app import app
from app import login

from . import connect_db, get_db, close_db, db
from flask import render_template, url_for, g, request, send_file, flash, redirect
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm, DataAccessForm, RegistrationForm
from app.models import User
from app.config import APP_TMP, Config

# WEBSITE PAGE ROUTES

# Home page route
@app.route('/')
def runit():
    with app.open_resource('static/descriptionText/HomeResearchDescription.txt') as f:
        content = f.read().decode('utf-8')
    return render_template('home.html', description=content)

# Login Page route
@app.route('/login/', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('runit'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('runit')
            return redirect(next_page)
    except Exception as e:
        print(e)
    return render_template('login.html', title='Sign In', form=form)

# Logout Page route
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('runit'))

# Registration route
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
            PLATE = form.Plate.data
            PLATE_Min = form.Plate_Min.data
            PLATE_Max = form.Plate_Max.data
            MJD = form.MJD.data
            MJD_Min = form.MJD_Min.data
            MJD_Max = form.MJD_Max.data
            FIBER = form.Fiber.data
            FIBER_Min = form.Fiber_Min.data
            FIBER_Max = form.Fiber_Max.data
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

            # Check Plate
            if(PLATE_Min and PLATE_Max):
                if(sql):
                    sql = sql + ' AND trim(PLATE) BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.PLATE BETWEEN %s AND %s'
                vars.append(PLATE_Min)
                vars.append(PLATE_Max)

            elif (PLATE_Min):
                if(sql):
                    sql = sql + ' AND trim(PLATE) >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.PLATE >= %s'
                vars.append(PLATE_Min)

            elif (PLATE_Max):
                if(sql):
                    sql = sql + ' AND trim(PLATE) <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.PLATE <= %s '
                vars.append(PLATE_Max)

            # Check MJD
            if(MJD_Min and MJD_Max):
                if(sql):
                    sql = sql + ' AND trim(MJD) BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.MJD BETWEEN %s AND %s'
                vars.append(MJD_Min)
                vars.append(MJD_Max)

            elif (MJD_Min):
                if(sql):
                    sql = sql + ' AND trim(MJD) >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.MJD >= %s'
                vars.append(MJD_Min)

            elif (MJD_Max):
                if(sql):
                    sql = sql + ' AND trim(MJD) <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.MJD <= %s '
                vars.append(MJD_Max)

            # Check FIBER
            if(FIBER_Min and FIBER_Max):
                if(sql):
                    sql = sql + ' AND trim(FIBER) BETWEEN %s AND %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.FIBER BETWEEN %s AND %s'
                vars.append(FIBER_Min)
                vars.append(FIBER_Max)

            elif (FIBER_Min):
                if(sql):
                    sql = sql + ' AND trim(FIBER) >= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.FIBER >= %s'
                vars.append(FIBER_Min)

            elif (FIBER_Max):
                if(sql):
                    sql = sql + ' AND trim(FIBER) <= %s'
                else:
                    sql = 'SELECT * FROM quasarinfo t1 inner join quasarinfo_table2 t2 on t1.QSO = t2.QSO WHERE t1.FIBER <= %s '
                vars.append(Fiber_Max)

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
@login_required
def test():
    return render_template('test.html', title='Test page')