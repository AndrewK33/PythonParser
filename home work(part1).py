import requests
import json
from pprint import pprint

service = f'https://api.github.com/users/bobuk/repos'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
           'Authorization':'Basic 7cf1865549f8175ce867a279a7b40fdcab7f4cc1'
           }
response = requests.get(service)
data = response.json()
with open ('response.json', 'w') as outfile:
    json.dump(response.json(), outfile)


