# MAIN ENGINE OF THE APPLICATION

# IMPORT FUNCTIONS FROM OTHER FILES
from backend import temp_find_interval

# LIBRARIES
from flask import Flask, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
import pandas as pd
import requests
from datetime import date, datetime
from pyhaystack.client.niagara import NiagaraHaystackSession
from pyhaystack.client.niagara import Niagara4HaystackSession
from bs4 import BeautifulSoup

# GLOBAL PARAMETERS - VALUES FOR OPERATORS (INITIALLY HAVEN'T SET YET)
ip = ''
station = ''
username = ''
password = ''
points = []
interval = 0
version = ''

# DEFAULT PARAMETERS FOR SERVER (INITIALLY HAVEN'T SET YET)
default_ip = ''
default_username = ''
default_password = ''

# CREATE FLASK APP, CONFIGURE SETTINGS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


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
# MAIN RESPONSE TO THE REQUEST
def index():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    # go to index.htmL
    return render_template("index.html", title="HOME")


# INITIATING SESSION I.E. DEFINING SESSION ATTRIBUTES
def session_init():
    session['login'] = False
    session['ip'] = ''
    session['version'] = '0'
    session['username'] = ''
    session['password'] = ''
    session['station'] = ''
    session['interval'] = '10'
    session['points'] = []
    # all possible stations for the currently choose station
    session["all_stations"] = []


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
# MAIN RESPONSE TO THE REQUEST
def login():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    global ip, version, username, password
    global default_ip, default_password, default_username
    form = LoginForm()
    # response depends on type of the request (GET or POST)
    if request.method == 'GET':
        # if just opens login page
        if session['login']:
            # if already log in, proceed to choosing of station/points
            return redirect(url_for("engineer"))
        else:
            # if not, go to the login page
            return render_template("login.html", title="Login", form=form, error=0, ip=default_ip,
                                   username=default_username, password=default_password)
    else:
        # if user pushes "Login"
        if check_login(request.form['ip'], request.form['username'], request.form['password']):
            # if login successful, then update session attributes
            session['login'] = True
            session['ip'] = request.form['ip']
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            if request.form.__contains__("remember_me"):
                # if "save as default", then update default variables
                default_ip = session['ip']
                default_username = session['username']
                default_password = session['password']
            # go to engineer page
            return redirect(url_for("engineer"))
        else:
            # if login failed, then go again to the login page (error=1, meaning their should be wrong message appeared)
            return render_template("login.html", title="Login", form=form, error=1)


# CHECKS IF LOGIN I SUCCESSFUL
def check_login(ip, username, password):
    global version
    # find code of the login page of the server
    text = requests.get("http://" + ip).text
    if text.__contains__("password"):
        # if this code contains "password" field, then it is NIAGARA AX
        version = '3'
    else:
        # if doesn't contain "password", then it is NIAGARA N4 (because it is pre-login page then)
        version = '4'
    # define version
    session['version'] = version
    if version == '3':
        # niagara AX authentication
        uri = "http://" + ip + "/login"
        session_ax = NiagaraHaystackSession(uri=uri, username=username, password=password, pint=True)
        au = session_ax.authenticate()
        cookie_id_ax = au.result[1]['niagara_session']
        cookies = {
            "niagara_login_state": "false",
            "niagara_login_state_data": "false",
            "niagara_session": cookie_id_ax,
        }
        url = "http://" + ip + "/obix/histories/"
        r = requests.get(url=url, cookies=cookies).text

        # find all possible stations for current station
        t = BeautifulSoup(r.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
        tags = t.find_all("ref")
        session["all_stations"] = []
        for tag in tags:
            session["all_stations"].append(tag["name"])

        return r.__contains__("histories")
    else:
        # niagara N4 authentication
        uri = "http://" + ip
        session_n4 = Niagara4HaystackSession(uri=uri, username=username, password=password, pint=True)
        op = session_n4.authenticate()
        op.wait()
        cookie_id_n4 = op.jsession
        cookies = {
            "niagara_userid": username,
            "JSESSIONID": cookie_id_n4
        }
        url = "http://" + ip + "/obix/histories/"
        r = requests.get(url=url, cookies=cookies).text

        # find all possible stations for current station
        t = BeautifulSoup(r.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
        tags = t.find_all("ref")
        session["all_stations"] = []
        for tag in tags:
            session["all_stations"].append(tag["name"])

        return r.__contains__("histories")


# LOG OUT FUNCTION
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    session['login'] = False
    return redirect(url_for("login"))


# ENGINEER PAGE
@app.route('/engineer/', methods=['GET', 'POST'])
def engineer():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    # if not login, go to login page
    if not session['login']:
        return redirect(url_for("login"))
    form = PointForm()
    # response depends on type of the request (GET or POST)
    if "GET" == request.method:
        # if just opens engineer page
        m = len(session['points'])
        stat = session['station']
        if stat == "":
            stat = session['all_stations'][len(session['all_stations']) - 1]
        return render_template("engineer.html", title="Set Report", form=form, points=session['points'], m=m,
                               interval=session['interval'], station=stat, ip=session['ip'])
    t = request.form.get("set_report")
    if t is None:
        # if pushes "Input Points" button (i.e. no "set_report" attribute yet in the form), just proceed with same page
        return '', 204
    else:
        # if pushes "Set Report" button, then update session attributes
        m = int(request.form['number'])
        session['interval'] = request.form['interval']
        session['station'] = request.form['station']
        session['points'] = []
        for i in range(1, m + 1):
            session['points'].append(request.form["point" + str(i)])
        global username, password, ip, station, version, interval, points
        # update operator variables
        username = session['username']
        password = session['password']
        ip = session['ip']
        version = session['version']
        station = session['station']
        interval = session['interval']
        points = session['points']
        # go to next page ("report set successfully")
        return set_report()


# "REPORT SUCCESSFULLY SET" PAGE
def set_report():
    return render_template("set_report.html", title="Report", points=points, interval=interval, ip=ip, station=station)


# OPERATOR PAGE
@app.route('/operator/', methods=['GET', 'POST'])
def operator():
    # initiate session if not yet
    if 'login' not in session:
        session_init()
    global points, interval, station, ip
    # find current date
    today = str(date.today())
    today_year = today[0:4]
    today_month = today[5:7]
    today_day = today[8:10]
    form = DateForm()
    if 'GET' == request.method:
        # if just opens operator page, return corresponding form (with some variables appearing there)
        return render_template("operator.html", title="Show Report", form=form, today_day=today_day,
                               today_month=today_month, today_year=today_year, points=', '.join(points),
                               interval=interval, ip=ip, station=station)
    else:
        # if pushes "Show Report" button, update operator variables
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']
        columns = request.form['columns']
        # define a period where to find recordings (i.e. "today", "lastWeek", etc.)
        period = set_period(year, month, day)
        # go to report page
        return show_report(period, year + "-" + month + "-" + day, int(columns))


# REPORT PAGE
def show_report(period, date, columns):
    global interval, points, station, ip, version
    # get one big report data-frame for given ip, station, period
    ds = temp_find_interval(username, password, points, period, date, interval, station, ip, version)
    # if returns string, means something went wrong (invalid station or points) and it returns wrong message
    if isinstance(ds, str):
        return render_template("wrong_input.html", title="Wrong Input", error_message=ds)
    # special case if no recordings
    if ds.empty:
        return render_template("show_report.html", title="Report Page", date=date, n_reports=0, columns_names_list=[],
                               row_data_list=[])
    # divide report into pages by number of columns per page
    reports = divide(ds, columns)
    n_reports = len(reports)
    # keep values in array variables..
    columns_names_list = []
    row_data_list = []
    for report in reports:
        columns_names_list.append(list(report.columns.values))
        row_data_list.append(report.values.tolist())
    # return report
    return render_template("show_report.html", title="Report Page", date=date, n_reports=n_reports,
                           columns_names_list=columns_names_list, row_data_list=row_data_list)


# FUNCTION TO DIVIDE REPORT INTO PAGES
def divide(ds, columns):
    reports = []
    columns_tot = len(ds.columns) - 1
    i = 0
    while columns_tot > columns:
        report = pd.concat([ds['Time'], ds[ds.columns[(columns * i + 1):(columns * (i + 1) + 1)]]], axis=1)
        columns_tot -= columns
        reports.append(report)
        i += 1
    reports.append(pd.concat([ds['Time'], ds[ds.columns[(columns * i + 1):len(ds.columns)]]], axis=1))
    return reports


# FUNCTION TO DEFINE TIME PERIOD WHERE TO FIND A RECORDING
def set_period(year, month, day):
    today = datetime.today()
    date = datetime(int(year), int(month), int(day))
    days_from_today = (today - date).days
    if days_from_today == 0:
        return 'today'
    if days_from_today == 1:
        return 'yesterday'
    if days_from_today <= today.weekday():
        return 'weekToDate'
    if days_from_today <= 7:
        return 'last7Days'
    if days_from_today <= 7 + today.weekday():
        return 'lastWeek'
    if date.month == today.month and date.year == today.year:
        return 'monthToDate'
    if date.month == today.month - 1 and date.year == today.year:
        return 'lastMonth'
    if date.month == 12 and today.month == 1 and date.year == today.year - 1:
        return 'lastMonth'
    if date.year == today.year:
        return 'yearToDate (limit=1000)'
    if date.year == today.year - 1:
        return 'lastYear (limit=1000)'
    return 'unboundedQuery'


# RUN THE APP ON THE SERVER
if __name__ == '__main__':
    app.run("0.0.0.0", "5000")
