from bottle import route, run, get, post, request
import random
from organizemongo import connectCollection, getPolarity
from bson.json_util import dumps
import json
from pymongo import MongoClient
import getpass
from datetime import datetime


password = getpass.getpass("Insert your AtlasMongoDB alvaro password: ")
connection = "mongodb+srv://alvaro:{}@apiproject-6gblk.mongodb.net/test?retryWrites=true&w=majority".format(
    password)
client = MongoClient(connection)
db, messages = connectCollection('chatNLPapi', 'messages', client)
_, users = connectCollection('chatNLPapi', 'users', client)
_, chats = connectCollection('chatNLPapi', 'chats', client)


'''class CollConection:

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
    '''Analiza con la librería Flair la emotividad de un chat concreto'''
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


# _, coll=creaclass('Prueba','datamad1019')esto solo era necesario si finalmente hago class
run(host='0.0.0.0', port=8080)
