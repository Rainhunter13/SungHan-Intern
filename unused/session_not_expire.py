from unused.input import cookie_id_My
import requests
import time

r = requests.Session()

cookies = {
    "niagara_userid": "admin",
    "JSESSIONID": cookie_id_My
}
cnt = 0
while True:
    GetObix = r.get(url = "http://192.168.0.198/obix/histories/rakhman_Station/", cookies = cookies)
    txt = GetObix.text
    if cnt%30==0:
        if txt.__contains__("ONOFF_01"):
            print("Time: " + str(cnt) + " seconds - SESSION WORKS")
        else:
            print("Time: " + str(cnt) + " seconds - SESSION FAILED")
    cnt+=10
    time.sleep(10)

