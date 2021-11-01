from pymongo import MongoClient, collation
def InjectToMongodb(articleList):
    client = MongoClient("mongodb+srv://capstoneuser:Capstone_IIITH@testingcluster.qv0hx.mongodb.net/capstone?retryWrites=true&w=majority")
    collection = client.capstone.news
    for article in articleList:
        if(not collection.find_one(article)):
            print(article)
            collection.insert_one(article)