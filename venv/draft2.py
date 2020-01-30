import requests
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPProxyAuth
r = requests.Session()

dataPostPrelogin = {
    'j_username': 'admin'
}

PostPrelogin = r.post(url = 'http://192.168.0.198/prelogin', data = dataPostPrelogin)
print(PostPrelogin.headers)
print(PostPrelogin.url)


AuthLogin = r.get("http://192.168.0.198/login", auth = HTTPDigestAuth('admin', 'adminMngr12345!'))
print(AuthLogin.headers)
print(AuthLogin.url)

AuthLogin = r.get("http://192.168.0.198/obix")
print(AuthLogin.headers)
print(AuthLogin.url)


AuthLogin = r.get("http://192.168.0.198/j_security_check", auth = HTTPDigestAuth('admin', 'adminMngr12345!'))
print(AuthLogin.headers)
print(AuthLogin.url)


AuthLogin = r.get("http://192.168.0.198/login", auth = HTTPProxyAuth('admin', 'adminMngr12345!'))
print(AuthLogin.headers)
print(AuthLogin.url)
