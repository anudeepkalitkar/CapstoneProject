from pymongo import MongoClient
def InjectToMongodb(articleList):
    client = MongoClient("mongodb+srv://capstoneuser:Capstone_IIITH@testingcluster.qv0hx.mongodb.net/capstone?retryWrites=true&w=majority")
    collection = client.capstone.news
    for article in articleList:
        collection.insert_many(article)
InjectToMongodb({'articleList':'test'})