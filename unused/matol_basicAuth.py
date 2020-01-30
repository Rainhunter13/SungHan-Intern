import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
r = requests.Session()

result = r.post(url = "http://matol.kz/j_spring_security_check", auth = HTTPBasicAuth('alihohl', 'rahman10'))
print(result.headers)
print(result.url)

main = r.get(url = "http://matol.kz")
if (main.text.__contains__("alihohl")):
    print("Login Successful")
else:
    print("Login Error")
