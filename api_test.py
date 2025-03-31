import http.client

conn = http.client.HTTPSConnection("api.github.com")
conn.request("GET", "/")
res = conn.getresponse()
print(f"Status: {res.status}, Response: {res.read().decode()}")
