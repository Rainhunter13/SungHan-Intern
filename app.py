# IMPORT FUNCTIONS FROM OTHER FILES
from temp_report import Temp_find_interval

# LIBRARIES
# flask python framework - main engine of the app
from flask import Flask, render_template, url_for, request, redirect, session
# flask support packages for working with forms (e.g. login form)
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
# to use pandas data-frames (convenient when working with tables)
import pandas as pd
# to make HTTP requests - to access data from web pages
import requests
# for accessing current date
from datetime import date, datetime
# for Niagara AX/N4 authentication
from pyhaystack.client.niagara import NiagaraHaystackSession
from pyhaystack.client.niagara import Niagara4HaystackSession
# for parsing data (from HTML code)
from bs4 import BeautifulSoup


# GLOBAL PARAMETERS - FOR OPERATORS
# initially haven't set yet (until first use of the application)
ip = ''
station = ''
username = ''
password = ''
points = []
interval = 0
version = ''

# DEFAULT PARAMETERS FOR SERVER
# initially haven't set yet
default_ip = ''
default_username = ''
default_password = ''


# CREATE FLASK APP, CONFIGURE SETTINGS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'   # secret key - any string you want


# CLASSES FOR HTTP FORMS
class DateForm(FlaskForm):
    submit = SubmitField('Show Report')


class PointForm(FlaskForm):
    submit = SubmitField('Set Report')


class LoginForm(FlaskForm):
    remember_me = BooleanField('Save as default')


# HOME PAGE
@app.route('/')
@app.route('/index/')
def index():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    return render_template("index.html", title="HOME")    # go to index.html


# initiating session i.e. define session attributes
def session_init():
    session['login'] = False
    session['ip'] = ''
    session['version'] = '0'
    session['username'] = ''
    session['password'] = ''
    session['station'] = ''
    session['interval'] = '10'
    session['points'] = []
    session["all_stations"] = []    # all possible stations for the currently choosen station


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    global ip, version, username, password
    global default_ip, default_password, default_username
    # create object of class LoginForm
    form = LoginForm()
    # response depends on type of the request
    if request.method == 'GET':
        # if user just opens login page
        if session['login']==True:
            # proceed to choosing of station/points if already log in
            return redirect(url_for("engineer"))
        else:
            # go to login.html if not log in (with some input variables: page title, form, error=1 if wrong password,
            # default server values)
            return render_template("login.html", title = "Login", form=form, error = 0, ip=default_ip, username=default_username, password=default_password)
    else:
        if check_login(request.form['ip'], request.form['username'], request.form['password']):
            session['login'] = True
            session['ip'] = request.form['ip']
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            if request.form.__contains__("remember_me"):
                default_ip = session['ip']
                default_username = session['username']
                default_password = session['password']
            return redirect(url_for("engineer"))
        else:
            return render_template("login.html", title="Login", form=form, error=1)

def check_login(ip, username, password):
    global version
    text = requests.get("http://" + ip).text
    if text.__contains__("password"):
        version='3'
    else:
        version='4'
    session['version'] = version
    if version=='3':
        uri = "http://" + ip + "/login"
        session_AX = NiagaraHaystackSession(uri=uri, username=username, password=password, pint=True)
        au = session_AX.authenticate()
        cookie_id_AX = au.result[1]['niagara_session']
        cookies = {
            #  niagara AX
            "niagara_login_state": "false",
            "niagara_login_state_data": "false",
            "niagara_session": cookie_id_AX,
        }
        url = "http://" + ip + "/obix/histories/"
        r = requests.get(url=url, cookies=cookies).text

        t = BeautifulSoup(r.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
        tags = t.find_all("ref")
        session["all_stations"] = []
        for tag in tags:
            session["all_stations"].append(tag["name"])

        return r.__contains__("histories")
    else:
        uri = "http://" + ip
        session_N4 = Niagara4HaystackSession(uri=uri, username=username, password=password, pint=True)
        op = session_N4.authenticate()
        op.wait()
        cookie_id_My = op.jsession
        cookies = {
            # niagara 4
            "niagara_userid": username,
            "JSESSIONID": cookie_id_My
        }
        url = "http://" + ip + "/obix/histories/"
        r = requests.get(url=url, cookies=cookies).text

        t = BeautifulSoup(r.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
        tags = t.find_all("ref")
        session["all_stations"] = []
        for tag in tags:
            session["all_stations"].append(tag["name"])

        return r.__contains__("histories")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not 'login' in session:
        session_init()
    session['login'] = False
    return redirect(url_for("login"))

@app.route('/operator/', methods=['GET', 'POST'])
def operator():
    if not 'login' in session:
        session_init()
    global points, inteval, station, ip
    today = str(date.today())
    today_year = today[0:4]
    today_month = today[5:7]
    today_day = today[8:10]
    form = DateForm()
    if (request.method=='GET'):
        return render_template("operator.html", title = "Show Report", form=form, today_day=today_day, today_month=today_month,
                               today_year=today_year, points=', '.join(points), interval = interval, ip=ip, station=station)
    else:
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        columns = request.form['columns']
        period = set_period(year, month, day)
        return show_report(period, year + "-" + month + "-" + day, int(columns))

def set_period(year, month, day):
    today = datetime.today()
    date = datetime(int(year), int(month), int(day))
    days_from_today = (today-date).days
    if days_from_today==0:
        return 'today'
    if days_from_today==1:
        return 'yesterday'
    if days_from_today<=today.weekday():
        return 'weekToDate'
    if days_from_today<=7:
        return 'last7Days'
    if days_from_today<=7+today.weekday():
        return 'lastWeek'
    if date.month==today.month and date.year==today.year:
        return 'monthToDate'
    if date.month==today.month-1 and date.year==today.year:
        return 'lastMonth'
    if date.month==12 and today.month==1 and date.year==today.year-1:
        return 'lastMonth'
    if date.year == today.year:
        return 'yearToDate (limit=1000)'
    if date.year == today.year- 1:
        return 'lastYear (limit=1000)'
    return 'unboundedQuery'

def show_report(period, date, columns):
    global interval, points, station, ip, version
    ds = Temp_find_interval(username, password, points, period, date, interval, station, ip, version)
    if isinstance(ds, str):
        return render_template("wrong_input.html", title="Wrong Input", error_message = ds)
    if ds.empty:
        return render_template("show_report.html", title="Report Page", date=date, n_reports=0, columns_names_list=[], row_data_list=[])
    reports = divide(ds, columns)
    n_reports = len(reports)
    columns_names_list = []
    row_data_list = []
    for report in reports:
        columns_names_list.append(list(report.columns.values))
        row_data_list.append(report.values.tolist())
    return render_template("show_report.html", title = "Report Page", date = date, n_reports = n_reports, columns_names_list=columns_names_list, row_data_list=row_data_list)

def divide(ds, columns):
    reports = []
    columns_tot = len(ds.columns) - 1
    i = 0
    while (columns_tot>columns):
        report = pd.concat([ds['Time'], ds[ds.columns[(columns*i+1):(columns*(i+1)+1)]]], axis=1)
        columns_tot -= columns
        reports.append(report)
        i+=1
    reports.append(pd.concat([ds['Time'],ds[ds.columns[(columns*i+1):len(ds.columns)]]], axis=1))
    return reports


@app.route('/engineer/', methods=['GET', 'POST'])
def engineer():
    if not 'login' in session:
        session_init()
    if (session['login']==False):
        return redirect(url_for("login"))
    form = PointForm()
    if (request.method=="GET"):
        m = len(session['points'])
        stat = session['station']
        if stat=="":
            stat = session['all_stations'][len(session['all_stations'])-1]
        return render_template("engineer.html", title = "Set Report", form = form, points = session['points'], m = m,
                               interval = session['interval'], station = stat, ip=session['ip'])
    t = request.form.get("set_report")
    if (t==None):
        return ('', 204)
    else:
        m = int(request.form['number'])
        session['interval'] = request.form['interval']
        session['station'] = request.form['station']
        session['points'] = []
        for i in range(1, m+1):
            session['points'].append(request.form["point"+str(i)])
        global username, password, ip, station, version, interval, points
        username = session['username']
        password = session['password']
        ip = session['ip']
        version = session['version']
        station = session['station']
        interval = session['interval']
        points = session['points']
        return set_report()

def set_report():
    return render_template("set_report.html", title = "Report", points = points, interval=interval, ip=ip, station=station)

if __name__ == '__main__':
    app.run("0.0.0.0", "5000")
