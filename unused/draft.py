import requests
from pyhaystack.client.niagara import Niagara4HaystackSession

uri1 = "http://192.168.0.198/"
username = "admin"
password = "adminMngr12345!"
import time

session = Niagara4HaystackSession(uri=uri1, username=username, password=password, pint=True)
op = session.authenticate()
op.wait()
print(op.jsession)
cookie_id_My = op.jsession
cookies = {
    "niagara_userid": username,
    "JSESSIONID": cookie_id_My
}
i = 0
cnt = 0
while True:
    r = requests.get(url="http://192.168.0.198/obix/histories/", cookies=cookies)
    txt = r.text
    print(str(i) + " more seconds: " + str(txt.__contains__("rakhman_Station")))
    i+=0.001
    time.sleep(i)