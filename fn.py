import flair
def connectCollection(database, collection,client):
    db = client[database]
    coll = db[collection]
    return db, coll
def getPolarity(sentence):
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
    s = flair.data.Sentence(sentence) #s es una instancia de esta clase
    flair_sentiment.predict(s) #s es transformada en esta línea
    return  s.labels
