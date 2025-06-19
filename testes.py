import requests

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMyIsImV4cCI6MTc1MDkwMzc1NX0.2UM4LEB4V0BMopJpyvmAfptdaj5AIFkXsCQkYoOBTIk'
}

requesicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(requesicao)
print(requesicao.json())