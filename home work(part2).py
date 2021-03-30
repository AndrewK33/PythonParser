import requests
import json
service = 'https://pokeapi.co/api/v2/pokemon/1'
req = requests.get(service)
data = json.loads(req.text)

#print (f"Покемон {data['name']} имеет способность {data['abilities'][0]['ability']['name']}")
with open ('req.json', 'w') as outfile:
        json.dump(req.json(), outfile)

