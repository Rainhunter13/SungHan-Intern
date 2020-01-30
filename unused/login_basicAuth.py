import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import pyhaystack

from getpass import getpass
r = requests.Session()

username ='admin'
password = 'adminMngr12345!'


# Accessing Obix to redirect to needed prelogin page
headersGetObix = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "192.168.0.198",
}
GetObix = r.get(url = "http://192.168.0.198/obix", headers = headersGetObix)
print(GetObix.status_code)
# print(GetPrelogin.text)
# Now on the prelogin page that is aiming to access Obix


# Inputting Username
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
# print(PostPrelogin.headers)
# print(PostPrelogin.text)
# Now on the login page that is aiming to access Obix

r.get("http://192.168.0.198/login")
print(r.cookies)
# Inputting password
headersGetLogin = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "http://192.168.0.198/login",
    "Host": "192.168.0.198"
}
GetLogin = r.get(url = 'http://192.168.0.198/j_security_check/', headers = headersGetLogin, auth = HTTPDigestAuth(username, password))
GetLogin = r.get(url = 'http://192.168.0.198/j_security_check/', headers = headersGetLogin)
print(GetLogin.status_code)
print(GetLogin.headers)
print(GetLogin.text[0:500])
print(r.cookies)


