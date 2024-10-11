import requests

# Gọi API để lấy danh sách học sinh đã được xếp hạng và sắp xếp
url = 'http://127.0.0.1:5000/get_sorted_ranks'
response = requests.get(url)
print(response.json())
