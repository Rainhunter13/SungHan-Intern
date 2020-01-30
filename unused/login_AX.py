import requests
from pyhaystack.client.niagara import NiagaraHaystackSession
from bs4 import BeautifulSoup

uri1 = "http://1.248.255.235/"
username = "admin"
password = "adminMngr12345!"

session= NiagaraHaystackSession(uri=uri1, username=username, password=password, pint=True)
op = session.authenticate()
print(op.result)
print(op)

cookie_id_AX = op.result[1]['niagara_session']
print(cookie_id_AX)
cookies = {
    #  niagara AX
    "niagara_login_state": "false",
    "niagara_login_state_data": "false",
    "niagara_session": cookie_id_AX,
}

url = "http://1.248.255.235/obix/histories/"
r = requests.get(url=url, cookies=cookies)
text = r.text

tool_soup = BeautifulSoup(text.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')
print(text)
t = tool_soup.find_all("ref")
print(t)
for x in t:
    print(x["name"])




