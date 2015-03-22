import json
from pymongo import MongoClient
from pprint import pprint

'''
json_data=open('nbateams.json')

listTeams = []
client = MongoClient()
db = client.nba
collection = db.teams
data = json.load(json_data)
for entry in data:
    collection.insert(entry)
    print entry['team_id']

print data
'''



'''
command = 'curl -H "Authorization: Lumpkins a324f56f-dc28-4b32-8e59-32dd9c093a4b" https://erikberg.com/nba/teams.json >> nbateams.json'




json_data.close()



from io import BytesIO
import pycurl
data = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://erikberg.com/nba/teams.json ')
c.setopt(c.WRITEFUNCTION, data.write)
c.perform()
c.close()

body = json.loads(data.getvalue())
team_list = []
for entry in body:
    print entry["team_id"]
    team_list.append(entry["team_id"])

c = pycurl.Curl()
for team in team_list:
    url = "https://erikberg.com/nba/roster/" + str(team) + ".json"
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    body = json.loads(data.getvalue())
    for entry in body:
        print entry
# Body is a string in some encoding.
# In Python 2, we can print it without knowing what the encoding is.
#print(body)
'''