import requests
import time
r = requests.Session()

cookies = {
    "niagara_userid": "admin",
    "JSESSIONID": "6e4b6b8e52f29fbf0137a240153e2998507215b09d6b855c15"
}
cnt = 0
while True:
    GetObix = r.get(url = "http://192.168.0.198/obix/histories/rakhman_Station/", cookies = cookies)
    txt = GetObix.text
    # uf
    # print(lol)
    if txt.__contains__("AHU1_ONOFF"):
        print("Time: " + str(cnt*30) + " seconds - SESSION WORKS")
    else:
        print("Time: " + str(cnt*30) + " seconds - SESSION FAILED")
    cnt+=1
    time.sleep(30)
