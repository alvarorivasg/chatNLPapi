from pymongo import MongoClient
from fn import connectCollection
import getpass
import json

#Get Password
password = getpass.getpass("Insert your AtlasMongoDB alvaro password: ")
connection = "mongodb+srv://alvaro:{}@apiproject-6gblk.mongodb.net/test?retryWrites=true&w=majority".format(password)

#Connect to DB and create collection with data from Felipe
client = MongoClient(connection)
db, messages = connectCollection('chatNLPapi','messages',client)

with open('input/samplechats.json') as f:
    chats_json = json.load(f)
messages.insert_many(chats_json)
datorg = list(messages.find({}))

#Create users collection
listusers=[]
for doc in range(len(datorg)):
    tup=(datorg[doc]["idUser"],datorg[doc]["userName"])
    listusers.append(tup)
listusers=set(listusers)
listusdic=[]
for us in listusers:
    dictus={}
    dictus["idUser"]=us[0]
    dictus["userName"]=us[1]
    listusdic.append(dictus)
with open('output/users.json', 'w') as fu:
    json.dump(listusdic,fu)
_, users = connectCollection('chatNLPapi','users',client)
with open('output/users.json') as f:
    usrs=json.load(f)
users.insert_many(usrs)

#Create chats collection
listchats=[]
for doc in range(len(datorg)):
    listchats.append(datorg[doc]['idChat'])
listchats=set(listchats)
listchatdic=[]
for ch in listchats:
    dictch={}
    dictch["idChat"]=ch
    listchatdic.append(dictch)
with open('output/chats.json', 'w') as fc:
    json.dump(listchatdic,fc)
_, chats = connectCollection('chatNLPapi','chats',client)
with open('output/chats.json') as f:
    chts=json.load(f)
chats.insert_many(chts)

#Link users,chats with messages
datusers = list(users.find({}))
us_ids = {}
for i in range(len(datusers)):
    us_ids[datusers[i]['idUser']]=datusers[i]["_id"]
for i in range(len(datorg)):
    query = {"$set":{'idUser':us_ids[datorg[i]['idUser']]}}
    messages.update_one(datorg[i],query)

data=list(messages.find({}))#por alguna razón que escapa a mi comprensión, he de regenerar esta query para que update_one funcione
datchats = list(chats.find({}))
ch_ids = {}
for i in range(len(datchats)):
    ch_ids[datchats[i]['idChat']]=datchats[i]["_id"]
for i in range(len(datorg)):
    query = {"$set":{'idChat':ch_ids[data[i]['idChat']]}}
    messages.update_one(data[i],query)
