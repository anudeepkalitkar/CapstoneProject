from pymongo import MongoClient
def InjectToMongodb(articleList):
    client = MongoClient("mongodb+srv://naveen:capstone@group32@cluster0.idvt3.mongodb.net/Capstone?retryWrites=true&w=majority")
    collection = client.news_articles.news_article
    for article in articleList:
        collection.insert_many(article)
