# INPUT INFORMATION

username = "admin"
session_id = "cc86e21e437e749cdb7903c717001af796bb596cef17ede10f"

tool_name = "Temp01"
period_name = "today"
# period_name = "yearToDate (limit=1000)"

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

cookies = {
    "niagara_userid": username,
    "JSESSIONID": session_id
}

# REQUEST TO 'ONNOF_01'
url = "http://192.168.0.198/obix/histories/rakhman_Station/" + tool_name
tool_req = requests.get(url = url, cookies = cookies)
tool_text = tool_req.text

# PARSE ONOFF_01 TO GET URL FOR 'TODAY'
tool_soup = BeautifulSoup(tool_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
# print(tool_soup)
tag = tool_soup.find(attrs = {'name' : period_name})
# print(tag['href'])
period_url = url + '/' + tag['href']
# print(period_url)

# REQUEST TO 'ONOFF-01'-'TODAY'
period_req = requests.get(url = period_url, cookies = cookies)
period_text = period_req.text

# PARSE 'ONOFF-01'-'TODAY' TO
period_soup = BeautifulSoup(period_text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
# print(period_soup)
obj = period_soup.find_all('obj')
del obj[0]
del obj[len(obj)-1]

time = []
location = []
value = []

for i in range(len(obj)):
    time.append(obj[i].abstime['val'])
    location.append(obj[i].abstime['tz'])
    value.append(float(obj[i].real['val']))
    # print(time[i] + "   " + location[i] + "   " + value[i])

# PUT DATA INTO THE PANDAS DATAFRAME
t = np.array(time)
l = np.array(location)
v = np.array(value)
data = np.array([t,l,v])
dataset = pd.DataFrame({'time': data[0, :], 'location': data[1, :], 'value': data[2, :]})
print(tool_name + " - " + period_name)
print(dataset)

print("max: " + str(np.amax(v)))
print("min: " + str(np.amin(v)))
print("mean: " + str(np.mean(v)))
