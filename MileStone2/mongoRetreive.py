from pymongo import MongoClient
import pandas as pd
import numpy as np
def GetFromMongodb(filter):
    client = MongoClient("mongodb+srv://naveen:itsmenaveen@cluster0.idvt3.mongodb.net/news_articles?retryWrites=true&w=majority")
    collection = client.news_articles.news_article
    cursor = collection.find(filter)
    return cursor

def SaveDataPandas(dataList, DataFields):
    arrayData = []
    for data in dataList:
        filteredData = []
        for field in DataFields:
            if(data[field]):
                filteredData.append(data[field])
            else:
                filteredData.append("")
        arrayData.append(filteredData)

    data = np.array(arrayData)
    return pd.DataFrame(data = data,columns=DataFields)
    
                
def retriveData(DataFields=["title","published_date","link","clean_url","summary","media","topic"] ):
    dataList = GetFromMongodb({})
    return SaveDataPandas(dataList, DataFields)
