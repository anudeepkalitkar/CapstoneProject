from pymongo import MongoClient
def InjectToMongodb(articleList):
    client = MongoClient("mongodb+srv://capstoneuser:Capstone_IIITH@testingcluster.qv0hx.mongodb.net/capstone?retryWrites=true&w=majority")
    collection = client.news_articles.news_article
    for article in articleList:
        collection.insert_many(article)
