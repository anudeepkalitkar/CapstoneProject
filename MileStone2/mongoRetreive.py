from pymongo import MongoClient
from pymongo.common import RETRY_WRITES
import yaml
def GetFromMongodb(filter):
    client = MongoClient("mongodb+srv://naveen:itsmenaveen@cluster0.idvt3.mongodb.net/news_articles?retryWrites=true&w=majority")
    collection = client.news_articles.news_article
    cursor = collection.find(filter)
    return cursor

def SaveDataArray(dataList, DataFields):
    arrayData = [DataFields]
    for data in dataList:
        filteredData = []
        for field in DataFields:
            filteredData.append(data[field])
        arrayData.append(filteredData)

    return arrayData
                

# dataList = GetFromMongodb({})
# DataFields = ["title","published_date","link","clean_url","summary","media","topic"]
# SaveDataArray(dataList, DataFields)
