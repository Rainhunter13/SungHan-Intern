import pyhaystack
import requests
from pyhaystack.client.niagara import Niagara4ScramAuthenticateOperation
from pyhaystack.client.niagara import Niagara4HaystackSession, HaystackSession
from pyhaystack.client.session import HaystackSession
from pyhaystack.client.http.base import HTTPClient

uri= "http://192.168.0.198/"
username = "admin"
password = "adminMngr12345!"

session = HaystackSession(uri=uri, api_dir="haystack")
print(session)
print(session.about())

print(pyhaystack.client.get_implementation("n4"))

# client = HTTPClient()
# r = client.request(method='POST', uri=uri+"prelogin", callback=None, body={"j_username":username})
# print(r)

un = Niagara4HaystackSession.unescape(password)
print(un)