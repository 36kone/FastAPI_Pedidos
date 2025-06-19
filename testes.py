import requests

headers = {
    'authorization': 'Bearer token'
}

requesicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(requesicao)
print(requesicao.json())
