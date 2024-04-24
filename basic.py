import requests

endpoint = "http://127.0.0.1:8081/comptes"
#response = requests.get(endpoint)
response = requests.post(endpoint, json={
        "numero_compte": 101,
        "client": 2,
        "solde": 0.00,})

print(response.json())

print(response.status_code)