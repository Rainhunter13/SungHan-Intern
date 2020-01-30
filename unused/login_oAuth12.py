import requests
import time
from requests.auth import HTTPDigestAuth

r = requests.Session()
username = 'admin'
password = 'adminMngr12345!'

# GET PRELOGIN
# headersGetPrelogin = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
#     "Accept-Encoding": "gzip, deflate",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "Host": "192.168.0.198",
#     "Cache-Control": "max-age=0"
# }
# GetPrelogin = r.get(url = "http://192.168.0.198/prelogin", headers = headersGetPrelogin)
# print(GetPrelogin.headers['Content-Length'])


# POST PRELOGIN
dataPostPrelogin = {
    'j_username': username
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


# GET LOGIN 1 - BASIC AUTH (W/ HEADERS)
headersGetLogin = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "text/html;charset=utf-8",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
GetLogin = r.get(url = 'http://192.168.0.198/j_security_check/', headers = headersGetLogin, auth = (username, password))
print(GetLogin.status_code)
print(GetLogin.history)
print(GetLogin.headers)

# POST LOGIN
# dataPostLogin = {
#     'j_password': password
# }
# headersPostLogin = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
#     "Accept-Encoding": "gzip, deflate",
#     "Referer": "http://192.168.0.198/login",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "Host": "192.168.0.198"
# }
# PostLogin = r.get(url = 'http://192.168.0.198/j_security_check/', data = dataPostLogin)
# print(PostLogin.headers['Set-cookie'])


# cookies = {
#     'niagara_userid':username,
#     'JSESSIONID':'f44dcabb7ec8c9af421c68f8814dbcae34f1bea9ddb19775cc'
# }
#


# GET LOGIN  - BASIC AUTH (W/O HEADERS)
# GetLogin = r.get(url = 'http://192.168.0.198/j_security_check/', cookies = PostPrelogin.cookies, auth = (username, password))
# print(GetLogin.headers['Set-cookie'])


# GET LOGIN - OAUTH1
# GetLogin = r.get(url = 'http://192.168.0.198/j_security_check/', auth = HTTPDigestAuth(username, password))
# print(GetLogin.headers['Set-cookie'])



# GET OBIX
headersGetObix = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://192.168.0.198/login",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "192.168.0.198"
}

text = r.get(url = "http://192.168.0.198/obix", headers = headersGetObix)
print(text.status_code)
print(text.text[0:500] + ' ...')