import requests

url = 'http://127.0.0.1:5000/submit_scores'
data = {
    'name': 'Nguyen Van A',
    'correct': 8,
    'total': 10
}

response = requests.post(url, json=data)
print(response.json())
