def connectCollection(database, collection,client):
    db = client[database]
    coll = db[collection]
    return db, coll