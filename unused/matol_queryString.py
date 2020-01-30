import requests
r = requests.Session()

# example: LOGIN INTO matol.kz WITH QUERY STRING PARAMS REQUEST --- DOESN'T WORK
data = {
    'username': 'alihohl',
    'password': 'rahman10',
    '_spring_security_remember_me': 'on',
    'prevPage': 'http://matol.kz/'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Host": "matol.kz",
    "Referer": "http://matol.kz/login/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "max-age=0"
}
result = r.get(url = "http://matol.kz/j_spring_security_check", params = data)
print(result.headers)
print(result.url)

main = r.get(url = "http://matol.kz")
if (main.text.__contains__("alihohl")):
    print("Login Successful")
else:
    print("Login Error")
