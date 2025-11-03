import requests
import json

# Login
url = 'http://127.0.0.1:8000/api/login/'
data = {'email': 'test@example.com', 'password': 'password123'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
print('Login Status Code:', response.status_code)
login_data = response.json()
print('Login Response:', login_data)

# Extract access token
access_token = login_data.get('access')
if access_token:
    # Chatbot with environmental question
    url = 'http://127.0.0.1:8000/api/chatbot/'
    data = {'message': 'What are the effects of climate change on oceans?'}
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Chatbot Status Code:', response.status_code)
    print('Chatbot Response:', response.json())

    # Chatbot with non-environmental question
    data = {'message': 'What is the capital of France?'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Chatbot Status Code for non-env:', response.status_code)
    print('Chatbot Response for non-env:', response.json())
else:
    print('No access token received')
