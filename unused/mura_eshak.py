from bs4 import BeautifulSoup

f = open("lol", encoding="utf-8")
s = f.read()
# print(s)

soup = BeautifulSoup(s.replace('\r', '').replace('\n', '').replace('\\', '').replace('rn', ''), 'html.parser')

x =  soup.find_all("string")
for i in range(len(x)):
    print(str(i+1) + ". " + x[i].text)
