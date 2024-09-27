import requests

url = "http://127.0.0.1:8080?power=20&VehAge=10&DrivAge=30&BonusMalus=10&VehGas=Regular&Area=D"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.request)
print(response.request.url)
print(response.request.body)
print(response.request.headers)
