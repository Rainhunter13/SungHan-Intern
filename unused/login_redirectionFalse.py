import requests
import time
from requests.auth import HTTPDigestAuth

username = 'admin'
password = 'adminMngr12345!'


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
PostPrelogin = requests.post(url = 'http://192.168.0.198/prelogin', headers = headersPostPrelogin, data = dataPostPrelogin)
print(PostPrelogin.headers['Set-Cookie'])


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
GetLogin = requests.get(url = 'http://192.168.0.198/j_security_check/', headers = headersGetLogin, auth = (username, password), allow_redirects = False)
print(GetLogin.headers)
print(GetLogin.text)




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

text = requests.get(url = "http://192.168.0.198/obix", headers = headersGetObix, cookies = GetLogin.cookies)
print(text.status_code)
print(text.text[0:500] + ' ...')