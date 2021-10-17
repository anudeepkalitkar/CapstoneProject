from pymongo import MongoClient
def InjectToMongodb(articleList):
    client = MongoClient("mongodb+srv://naveen:itsmenaveen@cluster0.idvt3.mongodb.net/news_articles?retryWrites=true&w=majority")
    collection = client.news_articles.news_article
    for article in articleList:
        collection.insert_one(article)