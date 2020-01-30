import requests
r = requests.Session()

username = 'admin'
password = 'adminMngr12345!'

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
# print(PostPrelogin.text)

payload =  {
    'j_username': username,
    'password': password
}
GetLogin = r.get('http://192.168.0.198/j_security_check/', params = payload)
print(GetLogin.headers)
print(GetLogin.url)
print(GetLogin.text[0:500])
