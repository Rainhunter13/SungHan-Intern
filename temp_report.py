import requests
from pyhaystack.client.niagara import NiagaraHaystackSession
from pyhaystack.client.niagara import Niagara4HaystackSession
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

dataset = pd.DataFrame([])

def cookie_id_AX(ip, username, password):
    uri = "http://" + ip + "/login"
    session_AX = NiagaraHaystackSession(uri=uri, username=username, password=password, pint=True)
    au = session_AX.authenticate()
    cookie_id_AX = au.result[1]['niagara_session']
    return cookie_id_AX

def cookie_id_N4(ip, username, password):
    uri = "http://" + ip
    session_N4 = Niagara4HaystackSession(uri=uri, username=username, password=password, pint=True)
    au = session_N4.authenticate()
    au.wait()
    cookie_id_N4 = au.jsession
    return cookie_id_N4

# RETURNS TWO-DIMENSIONAL ARRAY OF REPORT VALUES FOR CERTAIN IP, STATION, TIME PERIOD
def Temp_report(username, password, tool_name, period_name, station, ip, version):
    global dataset
    # LOGIN
    if version=="3":
        cookies = {
            #  niagara AX
            "niagara_login_state": "false",
            "niagara_login_state_data": "false",
            "niagara_session": cookie_id_AX(ip, username, password)
        }
    else:
        cookies = {
            #  niagara 4.0
            "niagara_userid": username,
            "JSESSIONID": cookie_id_N4(ip, username, password)
        }
        # print(cookies['JSESSIONID'])

    # FIND URL TO PARSE
    url = "http://" + ip + "/obix/histories/"

    r = requests.get(url=url, cookies=cookies).text
    t = BeautifulSoup(r.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    tags = t.find_all("ref")
    all_stations = []
    for tag in tags:
        all_stations.append(tag["name"])
    if not station in all_stations:
        return "Station '" + station + "' does not exist. Please check the spelling."

    url = url + station + "/" + tool_name
    tool_req = requests.get(url = url, cookies = cookies)
    tool_text = tool_req.text

    if not tool_text.__contains__("today"):
        return "Point '" + tool_name + "' does not exist. Please check the spelling."

    tool_soup = BeautifulSoup(tool_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    tag = tool_soup.find(attrs = {'name' : period_name})
    period_url = url + '/' + tag['href']

    # REQUEST DATA
    period_req = requests.get(url = period_url, cookies = cookies)
    period_text = period_req.text

    # PARSE FOR RECORDINGS INFORMATION
    period_soup = BeautifulSoup(period_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    obj = period_soup.find_all('obj')
    if len(obj)>0:
        del obj[0]
    if len(obj)>0:
        del obj[len(obj)-1]
    date = []
    time = []
    gmt = []
    location = []
    value = []
    for i in range(len(obj)):
        date.append(obj[i].abstime['val'][0:10])
        time.append(obj[i].abstime['val'][11:19])
        gmt.append(obj[i].abstime['val'][23:29])
        location.append(obj[i].abstime['tz'])
        value.append(format(float(obj[i].real['val']), ".2f"))

    # PUT DATA INTO THE TWO-DIMENSIONAL ARRAY
    d = np.array(date)
    t = np.array(time)
    g = np.array(gmt)
    l = np.array(location)
    v = np.array(value)
    data = np.array([d,t,g,l,v])
    data = np.transpose(data)
    return data

# RETURN DATAFRAME OF VALUES FOR SPECIFIC DATE
def Temp_find_date(username, password, Temp_point_name, Temp_period_name, date, station ,ip, version):
    data = Temp_report(username, password, Temp_point_name, Temp_period_name, station, ip, version)
    if isinstance(data, str):
        return data
    ans = []
    for i in range(len(data)):
        if data[i][0]==date:
            ans.append([data[i][1], data[i][4]])
    ans = pd.DataFrame(ans, columns=['Time', Temp_point_name])
    return ans

# SORTS REPORT DATAFRAME BY THE TIME INTERVAL
def Temp_find_interval(username, password, Temp_point_names, Temp_period_name, date, interval, station, ip, version):
    if len(Temp_point_names)==0:
        return pd.DataFrame([])
    ans = Temp_find_date(username, password, Temp_point_names[0], Temp_period_name, date, station, ip, version)
    if isinstance(ans, str):
        return ans
    for Temp_point_name in Temp_point_names:
        if Temp_point_name=="":
            continue
        x = Temp_find_date(username, password, Temp_point_name, Temp_period_name, date, station, ip, version)
        if isinstance(x, str):
            return x
        ans[Temp_point_name] = x[Temp_point_name]
    drop_rows = []
    for i in range(ans.shape[0]):
        if minutes(ans['Time'][i])%int(interval)!=0:
            drop_rows.append(i)
    ans = ans.drop(index = drop_rows, axis=0)
    return ans

# TRANSFORMS TIME INTO NUMBER OF MINUTES
def minutes(s):
    h = int(s[0:2])
    m = int(s[3:5])
    return 60*h+m







# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST

# Temp_report(username, password, "Temp01", Temp_period_name)
# print(dataset)
# print()

# REPORT EXAMPLE
# print("Recordings for the date " + date + " for points in " + str(Temp_point_names) + ":")
# print()
# ds = Temp_find_recordings(username, password, Temp_point_names, Temp_period_name, date)
# print(ds)