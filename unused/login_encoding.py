import requests
r = requests.Session()


username ='admin'
password = 'adminMngr12345!'
encoded_pw = 'm29FOvF4oaxv8b4LSvPhqA=='



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
print(GetObix.url)
print(GetObix.headers)



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
print(PostPrelogin.url)
print(PostPrelogin.headers)



dataPostLogin = {
    'action': 'sendClientFirstMessage&clientFirstMessage=n',
    'n': username,
    'r': encoded_pw
}
headersPostLogin = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "192.168.0.198"
}
PostLogin = r.post(url = 'http://192.168.0.198/login', headers = headersPostLogin, data = dataPostLogin)
print(PostLogin.url)
print(PostLogin.headers)
print(PostLogin.cookies)

GetObix = r.get(url = "http://192.168.0.198/obix/histories/rakhman_Station/")
print(GetObix.text[0:300])