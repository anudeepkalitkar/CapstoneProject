import requests

def GetRapidAPIFeed(queryString):
    attributeList = ["title","published_date","link","clean_url","summary","media","topic"]
    url = "https://free-news.p.rapidapi.com/v1/search"
    querystring = {"q":queryString, "lang":"en"}
    headers = {
    'x-rapidapi-host': "free-news.p.rapidapi.com",
    'x-rapidapi-key': "a48e1080cbmsh82d6dc13a706169p15e1e6jsn1d52942e5af9"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = response.json()
    articleList = []
    try:
        for article in json_response["page_size"]:
            articleData = {}
            for items in attributeList:
                articleData[items] = article[items]
            articleList.append(articleData)
        return articleList
    except:
        return None

def GetRapidAPIData(queryStringList):
    articleList = []
    for queryString in queryStringList:
        articles = GetRapidAPIFeed(queryString)
        if(articles):
            articleList.append(articles)
    return articleList
        
