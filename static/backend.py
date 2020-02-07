# MAIN FUNCTIONS IMPLEMENTATION

# LIBRARIES
import requests
from pyhaystack.client.niagara import NiagaraHaystackSession
from pyhaystack.client.niagara import Niagara4HaystackSession
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep


# AUTHENTICATION FOR NIAGARA AX - RETURNS SESSION ID
def session_id_ax(ip, username, password):
    uri = "http://" + ip + "/login"
    session_ax = NiagaraHaystackSession(uri=uri, username=username, password=password, pint=True)
    au = session_ax.authenticate()
    return au.result[1]['niagara_session']


# AUTHENTICATION FOR NIAGARA N4 - RETURNS SESSION ID
def session_id_n4(ip, username, password):
    uri = "http://" + ip
    session_n4 = Niagara4HaystackSession(uri=uri, username=username, password=password, pint=True)
    au = session_n4.authenticate()
    au.wait()
    return au.jsession


# RETURNS COOKIES FROM AUTHENTICATION
def set_cookies(ip, username, password, version):
    if version == "3":
        #  niagara AX
        cook = {
            "niagara_login_state": "false",
            "niagara_login_state_data": "false",
            "niagara_session": session_id_ax(ip, username, password)
        }
    else:
        #  niagara N4
        cook = {
            "JSESSIONID": session_id_n4(ip, username, password),
            "niagara_userid": username
        }
    return cook


# RETURNS TWO-DIMENSIONAL ARRAY OF REPORT VALUES FOR GIVEN CERTAIN IP, STATION, TIME PERIOD
def report_table(username, password, tool_name, period_name, station, ip, version):
    # get cookies from authentication
    cookies = set_cookies(ip, username, password, version)
    i = 0.1
    while not requests.get(url="http://" + ip + "/obix/histories/", cookies=cookies).text.__contains__("histories"):
        # if cookies were set not correctly, reset them (it could happens sometimes)
        print("request error")
        cookies = set_cookies(ip, username, password, version)
        i*=2
        sleep(i)
        if i>5:
            return "Connection error. Please, try again."

    # check is station exists (check ../histories for all stations)
    url = "http://" + ip + "/obix/histories/"
    r = requests.get(url=url, cookies=cookies)
    tx = r.text
    t = BeautifulSoup(tx.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    tags = t.find_all("ref")
    all_stations = []
    for tag in tags:
        all_stations.append(tag["name"])
    if station not in all_stations:
        return "Station '" + station + "' does not exist. Please check the spelling."

    # check if point exists (try to access ../station/point and see if error)
    url = url + station + "/" + tool_name
    tool_req = requests.get(url=url, cookies=cookies)
    tool_text = tool_req.text
    if not tool_text.__contains__("today"):
        return "Point '" + tool_name + "' does not exist. Please check the spelling."

    # find the url for required period (e.g. link for "today" is sth like "../~historyQuery?start=2020-01-31T00:00:...")
    tool_soup = BeautifulSoup(tool_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''),
                              'html.parser')
    tag = tool_soup.find(attrs={'name': period_name})
    period_url = url + '/' + tag['href']

    # main request for recordings page
    period_req = requests.get(url=period_url, cookies=cookies)
    period_text = period_req.text
    return parse(period_text)


# RETURNS TWO-DIMENSIONAL ARRAY OF REPORT VALUES FOR GIVEN REQUEST RESPONSE TEXT (HTML)
def parse(period_text):
    # parse for recordings values
    period_soup = BeautifulSoup(period_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''),
                                'html.parser')
    objs = period_soup.find_all('obj')
    if len(objs) > 0:
        del objs[0]
    if len(objs) > 0:
        del objs[len(objs) - 1]
    date = []
    time = []
    gmt = []
    location = []
    value = []
    for i in range(len(objs)):
        date.append(objs[i].abstime['val'][0:10])
        time.append(objs[i].abstime['val'][11:19])
        gmt.append(objs[i].abstime['val'][23:29])
        location.append(objs[i].abstime['tz'])
        value.append(format(float(objs[i].real['val']), ".2f"))

    # put data into two dimensional array
    d = np.array(date)
    t = np.array(time)
    g = np.array(gmt)
    l = np.array(location)
    v = np.array(value)
    data = np.array([d, t, g, l, v])
    data = np.transpose(data)
    return data


# RETURN DATA-FRAME OF VALUES FOR SPECIFIC DATE
def sort_by_date(username, password, temp_point_name, temp_period_name, date, station, ip, version):
    data = report_table(username, password, temp_point_name, temp_period_name, station, ip, version)
    if isinstance(data, str):
        return data
    ans = []
    for i in range(len(data)):
        if data[i][0] == date:
            ans.append([data[i][1], data[i][4]])
    ans = pd.DataFrame(ans, columns=['Time', temp_point_name])
    return ans


# SORTS REPORT DATA-FRAME BY THE TIME INTERVAL
def sort_by_interval(username, password, temp_point_names, temp_period_name, date, interval, station, ip, version, ignore_seconds):
    # if no points inputted
    if len(temp_point_names) == 0:
        return "No points to show."
    ans = sort_by_date(username, password, temp_point_names[0], temp_period_name, date, station, ip, version)
    # if invalid input - i.e. returns wrong message
    if isinstance(ans, str):
        return ans
    # concatenate all arrays for all points into one data-frame
    for i in range(1, len(temp_point_names)):
        temp_point_name = temp_point_names[i]
        if temp_point_name == "":
            continue
        x = sort_by_date(username, password, temp_point_name, temp_period_name, date, station, ip, version)
        if isinstance(x, str):
            return x
        ans[temp_point_name] = x[temp_point_name]
    # drop row if corresponding time doesn't match the interval
    drop_rows = []
    for i in range(ans.shape[0]):
        if ignore_seconds:
            ans['Time'][i] = ans['Time'][i][0:6] + "00"
        if minutes(ans['Time'][i]) % int(interval) != 0:
            drop_rows.append(i)
    ans = ans.drop(index=drop_rows, axis=0)
    return ans


# TRANSFORMS TIME INTO NUMBER OF MINUTES
def minutes(s):
    h = int(s[0:2])
    m = int(s[3:5])
    return 60 * h + m
