import requests

endpoint = "http://127.0.0.1:8081/login"
#response = requests.get(endpoint)
response = requests.post(endpoint, json={
        "username": "elhadji            ",
        "password": "elhadjisarr",})

print(response.json())

print(response.status_code)