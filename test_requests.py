import requests

url = 'http://localhost:5000/get_form'

data = {
    'email': 'example@example.com',
    'message': 'Hello, this is a test message.'
}

response = requests.post(url, data=data)
print(response.json())

data = {
    'order_date': '2023-10-01',
    'customer_name': 'John Doe',
    'phone_number': '+7 123 456 7890'
}

response = requests.post(url, data=data)
print(response.json())

data = {
    'unknown_field': 'some text',
    'another_unknown_field': '12/34/5678'
}

response = requests.post(url, data=data)
print(response.json())