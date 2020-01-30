import requests
import time
r = requests.Session()




headersGetPrelogin = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "192.168.0.198",
    "Cache-Control": "max-age=0"
}
GetPrelogin = r.get(url = "http://192.168.0.198/prelogin", headers = headersGetPrelogin)
print(GetPrelogin.headers)




dataPostPrelogin = {
    'j_username': 'admin'
}
headersPostPrelogin = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "192.168.0.198"
}
PostPrelogin = r.post(url = 'http://192.168.0.198/prelogin', headers = headersPostPrelogin, data = dataPostPrelogin)
print(PostPrelogin.headers)

time.sleep(1)



r.auth = ('admin', 'adminMngr12345!')
auth = r.post('http://192.168.0.198')
response = r.get('http://192.168.0.198/login')
print(response.status_code)
print(response.headers)