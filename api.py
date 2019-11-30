from bottle import route, run, get, post, request
import random
from organizemongo import connectCollection
import bson
from pymongo import MongoClient
import getpass


password = getpass.getpass("Insert your AtlasMongoDB alvaro password: ")
connection = "mongodb+srv://alvaro:{}@apiproject-6gblk.mongodb.net/test?retryWrites=true&w=majority".format(password)
client= MongoClient(connection)
db, messages = connectCollection('chatNLPapi','messages',client)
_, users = connectCollection('chatNLPapi','users',client)
_, chats = connectCollection('chatNLPapi','chats',client)


@get("/")
def index():
    return {
        "nombre": random.choice(["Pepe", "Juan", "Fran", "Luis"])
    }


@get("/chiste/<tipo>")
def demo2(tipo):
    print(f"un chiste de {tipo}")
    if tipo == "chiquito":
        return {
            "chiste": "Van dos soldados en una moto y no se cae ninguno porque van soldados"
        }
    elif tipo == "eugenio":
        return {
            "chiste": "Saben aquell que diu...."
        }
    else:
        return {
            "chiste": "No puedorrr!!"
        }

@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms["autor"]
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}


#_, coll=creaclass('Prueba','datamad1019')esto solo era necesario si hago class
run(host='0.0.0.0', port=8080)