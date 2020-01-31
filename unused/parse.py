from unused.input import cookie_id
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

Temp_gmin = 0
Temp_gmax = 0
Temp_gmean = 0
ONOFF_gtrue = 0
ONOFF_gfalse = 0

def session_id(password):
    return cookie_id

# FULL REPORT FOR ONOFF
def ONOFF_report(username, password, tool_name, period_name):
    # REQUEST TO 'ONOFF_0*'
    cookies = {
        "niagara_userid": username,
        "JSESSIONID": session_id(password)
    }
    url = "http://192.168.0.198/obix/histories/rakhman_Station/" + tool_name
    tool_req = requests.get(url = url, cookies = cookies)
    tool_text = tool_req.text

    # PARSE ONOFF_0* TO GET URL FOR 'TODAY'
    tool_soup = BeautifulSoup(tool_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    tag = tool_soup.find(attrs = {'name' : period_name})
    period_url = url + '/' + tag['href']

    # REQUEST TO 'ONOFF_0*'-'PERIOD'
    period_req = requests.get(url = period_url, cookies = cookies)
    period_text = period_req.text

    # PARSE 'ONOFF-01'-'PERIOD' TO OBTAIN DATA
    period_soup = BeautifulSoup(period_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    obj = period_soup.find_all('obj')
    del obj[0]
    del obj[len(obj)-1]
    date = []
    time = []
    gmt = []
    location = []
    value = []
    for i in range(len(obj)):
        date.append(obj[i].abstime['val'][0:10])
        time.append(obj[i].abstime['val'][11:23])
        gmt.append(obj[i].abstime['val'][23:29])
        location.append(obj[i].abstime['tz'])
        value.append(obj[i].bool['val'])

    # PUT DATA INTO THE PANDAS DATAFRAME
    d = np.array(date)
    t = np.array(time)
    g = np.array(gmt)
    l = np.array(location)
    v = np.array(value)
    data = np.array([d,t,g,l,v])
    dataset = pd.DataFrame({'date': data[0, :], 'time': data[1, :], 'GMT': data[2, :], 'location': data[3, :], 'value': data[4, :]})

    # COMPUTE NUMBER OF TRUE AND FALSES
    global ONOFF_gtrue
    global ONOFF_gfalse
    ONOFF_gtrue = 0
    ONOFF_gfalse = 0
    for i in v:
        if i=='true':
            ONOFF_gtrue +=1
        else:
            ONOFF_gfalse +=1

    return dataset

# FULL REPORT FOR Temp
def Temp_report(username, password, tool_name, period_name):
    # REQUEST TO 'ONOFF_0*'
    cookies = {
        "niagara_userid": username,
        "JSESSIONID": session_id(password)
    }
    url = "http://192.168.0.198/obix/histories/rakhman_Station/" + tool_name
    tool_req = requests.get(url = url, cookies = cookies)
    tool_text = tool_req.text

    # PARSE ONOFF_0* TO GET URL FOR 'TODAY'
    tool_soup = BeautifulSoup(tool_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    tag = tool_soup.find(attrs = {'name' : period_name})
    period_url = url + '/' + tag['href']

    # REQUEST TO 'ONOFF_0*'-'PERIOD'
    period_req = requests.get(url = period_url, cookies = cookies)
    period_text = period_req.text

    # PARSE 'ONOFF-01'-'PERIOD' TO OBTAIN DATA
    period_soup = BeautifulSoup(period_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
    obj = period_soup.find_all('obj')
    del obj[0]
    del obj[len(obj)-1]
    date = []
    time = []
    gmt = []
    location = []
    value = []
    for i in range(len(obj)):
        date.append(obj[i].abstime['val'][0:10])
        time.append(obj[i].abstime['val'][11:23])
        gmt.append(obj[i].abstime['val'][23:29])
        location.append(obj[i].abstime['tz'])
        value.append(float(obj[i].real['val']))

    # PUT DATA INTO THE PANDAS DATAFRAME
    d = np.array(date)
    t = np.array(time)
    g = np.array(gmt)
    l = np.array(location)
    v = np.array(value)
    data = np.array([d,t,g,l,v])
    dataset = pd.DataFrame({'date': data[0, :], 'time': data[1, :], 'GMT': data[2, :], 'location': data[3, :], 'value': data[4, :]})

    #COMPUTE MIN, MAX, MEAN
    global Temp_gmax
    global Temp_gmin
    global Temp_gmean
    Temp_gmax = np.amax(v)
    Temp_gmin = np.amin(v)
    Temp_gmean = np.mean(v)

    return dataset

# COUNTS NUMBER OF TRUE AND FALSE IN THE DATA
def ONOFF_count():
    global ONOFF_gtrue
    global ONOFF_gfalse
    return (ONOFF_gfalse, ONOFF_gtrue)

# COUNTS MAX, MIN, MEAN OF THE VALUES
def Temp_max():
    global Temp_gmax
    return Temp_gmax

def Temp_min():
    global Temp_gmin
    return Temp_gmin

def Temp_mean():
    global Temp_gmean
    return Temp_gmean

# TRANSFORMS TIME TO THE TIMESTAMP WHICH IS USEFUL FOR TIME COMPARING
def timestamp(time):
    hours = int(time[0:2])
    minutes = int(time[3:5])
    seconds = int(time[6:8])
    miliseconds = int(time[9:12])
    return hours*60*60*60+minutes*60*60+seconds*60+miliseconds

# FINDS THE VALUE OF RECORDING THAT IS MOST NEAREST TO THE REQUIRED TIME (FOR ONOFF)
def ONOFF_find_value(username, password, tool_name, period_name, date, time):
    dataset = ONOFF_report(username, password, tool_name, period_name)
    d = dataset['date']
    pos_ind = []
    for i in range(d.size):
        if (d[i]==date):
            pos_ind.append(i)
    if (len(pos_ind)==0):
        return ("No recordings at " + date)
    pos_time = []
    indices = []
    for i in pos_ind:
        pos_time.append(timestamp(dataset['time'][i]))
        indices.append(i)
    t = timestamp(time)
    i = 0
    while (t > pos_time[i]):
        i+=1
    if (i==0):
        return (dataset['time'][indices[i]], dataset['value'][indices[i]])
    else:
        if (pos_time[i]-t < t-pos_time[i-1]):
            return (dataset['time'][indices[i]], dataset['value'][indices[i]])
        else:
            return (dataset['time'][indices[i-1]], dataset['value'][indices[i-1]])

# FINDS THE VALUE OF RECORDING THAT IS MOST NEAREST TO THE REQUIRED TIME (FOR Temp)
def Temp_find_value(username, password, tool_name, period_name, date, time):
    dataset = Temp_report(username, password, tool_name, period_name)
    d = dataset['date']
    pos_ind = []
    for i in range(d.size):
        if (d[i]==date):
            pos_ind.append(i)
    if (len(pos_ind)==0):
        return ("No recordings at " + date)
    pos_time = []
    indices = []
    for i in pos_ind:
        pos_time.append(timestamp(dataset['time'][i]))
        indices.append(i)
    t = timestamp(time)
    i = 0
    while (t > pos_time[i]):
        i+=1
    if (i==0):
        return (dataset['time'][indices[i]], dataset['value'][indices[i]])
    else:
        if (pos_time[i]-t < t-pos_time[i-1]):
            return (dataset['time'][indices[i]], dataset['value'][indices[i]])
        else:
            return (dataset['time'][indices[i-1]], dataset['value'][indices[i-1]])


# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST
username = "admin"
password = "adminMngr12345!"

ONOFF_point_name = "ONOFF_01"
ONOFF_period_name = "today"
ONOFF_date = "2020-01-02"
ONOFF_time = "06:25:56.347"

Temp_point_name = "Temp01"
Temp_period_name = "last7Days"
Temp_date = "2019-12-29"
Temp_time = "05:35:00.008"

print(ONOFF_point_name + " - " + ONOFF_period_name + ":")
print(ONOFF_report(username, password, ONOFF_point_name, ONOFF_period_name))
print()

print("True: " + str(ONOFF_count()[1]) + " values")
print("False: " + str(ONOFF_count()[0]) + " values")
print()

print(Temp_point_name + " - " + Temp_period_name + ":")
df = Temp_report(username, password, Temp_point_name, Temp_period_name)
print(Temp_report(username, password, Temp_point_name, Temp_period_name))
print()

print("max: " + str(Temp_max()))
print("min: " + str(Temp_min()))
print("mean: " + str(Temp_mean()))
print()

x = ONOFF_find_value(username, password, ONOFF_point_name, ONOFF_period_name, ONOFF_date, ONOFF_time)
print("Finding recording for:   " + ONOFF_point_name + " " + ONOFF_period_name + " "+ ONOFF_date + " " + ONOFF_time + "   ...")
print("The most nearest recording time is:   " + str(x[0]) + " with the value of:   " + str(x[1]))
print()

x = Temp_find_value(username, password, Temp_point_name, Temp_period_name, Temp_date, Temp_time)
print("Finding recording for:   " + Temp_point_name + " " + Temp_period_name + " " + Temp_date + " " + Temp_time + "   ...")
print("The most nearest recording time is:   " + str(x[0]) + " with the value of:   " + str(x[1]))
print()