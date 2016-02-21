import httplib
import json

connection = httplib.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '881fc6e02a994d938891a3c0df48d4cf', 'X-Response-Control': 'minified' }
connection.request('GET', '/v1/fixtures', None, headers )
response = json.loads(connection.getresponse().read().decode())

print (response)