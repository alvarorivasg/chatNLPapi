from bottle import route, run, get, post, request, HTTPResponse
import random
from fn import connectCollection,getPolarity
from bson.json_util import dumps
import json
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import pandas as pd
load_dotenv()

connection = os.getenv('CONNECTIONMONGO')
client = MongoClient(connection)
db, messages = connectCollection('chatNLPapi', 'messages', client)
_, users = connectCollection('chatNLPapi', 'users', client)
_, chats = connectCollection('chatNLPapi', 'chats', client)


'''
Pa futuras actualizaciones: montar esto como clase y en las funciones decoradas llamar a métodos de la clase

class CollConnection:

    def __init__(self,dbName,collection):
        self.client = MongoClient()
        self.db = self.client[dbName]
        self.collection=self.db[collection]

coll=CollConection('Prueba','datamad1019')'''


@get("/prueba")
def test():
    return {"Connected"}


@get("/chat/<idChat>")
def getChat(idChat):
    '''
    idChat must be an integer
    '''
    chatid = list(chats.find({'idChat': int(idChat)}))[0]['_id']
    datachat = list(messages.find({'idChat': chatid}))
    rtrn = {}
    for i in range(len(datachat)):
        name = datachat[i]['userName']
        message = datachat[i]['text']
        datetime = datachat[i]['datetime']
        rtrn[f'message {i+1}'] = name, message, datetime
    return dumps(rtrn)


@get("/users")
def getUsers():
    return dumps(users.find({}))


@post('/create/user')
def createUser():
    '''Recibe parámetros de la siguiente estructura: {'name': 'Pepe'}'''
    new_id = max(users.distinct("idUser")) + 1
    name = request.forms["name"]
    new_user = {
        "idUser": new_id,
        "userName": name
    }
    return {"Succesfully inserted": str(users.insert_one(new_user).inserted_id)}


@post('/create/chat')
def createChat():
    '''Recibe como parámetros un diccionario vacío'''
    new_id = max(chats.distinct("idChat")) + 1
    new_chat = {
        "idChat": new_id,
    }
    return {"Succesfully inserted": str(chats.insert_one(new_chat).inserted_id)}


@post('/create/message')
def createMessage():
    '''Recibe como parámetros la siguiente estructura:
    {"userName":,"idChat":,"text":}
    Nota: si el idChat introducido como parámetro no existe, se creará un nuevo idChat con un número
    distinto al introducido. Ver createChat'''
    user = list(users.find({'userName': request.forms['name']}))
    if len(user) == 0:
        createUser()
        userid = list(users.find({'userName': request.forms['name']}))[
            0]['_id']
    else:
        userid = user[0]['_id']
    try:
        chat = list(chats.find({'idChat': int(request.forms['idChat'])}))
    except:
        pass
    if 'idChat' not in request.forms.keys() or len(chat) == 0:
        createChat()
        chatid = list(chats.find({'idChat': max(chats.distinct("idChat"))}))[0]['_id']
    else:
        chatid = chat[0]['_id']
    rtrn = {'idUser': userid, 'userName': request.forms['name'],
            'idMessage': max(messages.distinct('idMessage')) + 1,
            'idChat': chatid,'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': request.forms['text']}
    messages.insert_one(rtrn)
    return dumps(rtrn)

@get('/analyze/<idChat>')
def anChat(idChat):
    data=list(chats.find({}))
    if str(idChat) not in list(set([str(ch['idChat']) for ch in data])):
        return HTTPResponse(status=200, body=json.dumps({'Message':'Chat ID not valid. Please try again'}))
    chat=json.loads(getChat(idChat))
    pols=[]
    for mes in chat:
        y=getPolarity(chat[mes][1])
        pols.append(y)
    cleanpols=list(map(lambda e: float(str(e)[11:-2]) if str(e)[1:4]=='POS' else float('-'+str(e)[11:-2]),pols))
    nicemen=cleanpols.index(max(cleanpols))
    badmen=cleanpols.index(min(cleanpols))
    rtrn={'Best vibing message': chat[list(chat.keys())[nicemen]][1],
    'Worst vibing message': chat[list(chat.keys())[badmen]][1],
    'Average polarity': sum(cleanpols)/len(cleanpols)}
    return dumps(rtrn)

@get("/recommend/<userName>")
def recommend(userName):
    data=list(messages.find({}))
    if userName not in list(set([us['userName'] for us in data])):
        return HTTPResponse(status=200, body=json.dumps({'Message':'User not valid. Please try again'}))
    words={}
    for men in data:
        if men['userName'] not in words.keys():
            words[men['userName']]=men['text']
        else:
            words[men['userName']]=words[men['userName']]+men['text']
    count_vectorizer = CountVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(words.values())
    words_matrix = sparse_matrix.todense()
    df = pd.DataFrame(words_matrix, columns=count_vectorizer.get_feature_names(), index=words.keys())
    similarity_matrix = distance(df, df)
    sim_df = pd.DataFrame(similarity_matrix, columns=words.keys(), index=words.keys())
    rtrn={f'Most similar users to {userName}': list(sim_df[userName].sort_values(ascending=False)[1:4].keys())}
    return dumps(rtrn)




# _, coll=collConnection('Prueba','datamad1019')esto solo era necesario si finalmente hago class
port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)
