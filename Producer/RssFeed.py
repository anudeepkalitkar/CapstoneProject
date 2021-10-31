import requests
from bs4 import BeautifulSoup

def GetRssFeedUrls(rssSource):
    res = requests.get(rssSource['rssPage'])
    content = BeautifulSoup(res.content, features='lxml')
    allLinks = content.find_all('a')
    rssData = []
    ExceptRSS = ['Most Recent Stories', 'Top Stories']
    for link in allLinks:
        if(link.text not in ExceptRSS and rssSource['rssLinkFilter'] in link['href']):
            try:
                rssData.append({'topic': link.text, 'link': link['href'], 'homePage': rssSource['homePage']}) 
            except:
                pass
    return rssData

def GetRssFeedData(rssData):
    res = requests.get(rssData['link'])
    content = BeautifulSoup(res.content, features='xml')
    articles = content.findAll('item')
    articleList = []
    attributesList = [
    {'name':'title', 'rssName': 'title'},
    {'name':'summary', 'rssName': 'description'},
    {'name':'link', 'rssName': 'link'},
    {'name':'published_date', 'rssName': 'pubDate'}
    ]
    for article in articles:
        articleData = {}
        for attribute in attributesList:
            try:
                articleData[attribute['name']] = article.find(attribute['rssName']).text
            except:
                articleData[attribute['name']] = None
        pass
        articleData['clean_url'] = rssData['homePage']
        articleData['topic'] = rssData['topic']
        articleData['media'] = None
        articleList.append(articleData)
    return articleList

def GetRssData(rssSources):
    articleList = []
    for rssSource in rssSources:
        rssDataSet = GetRssFeedUrls(rssSource)
        for rssData in rssDataSet:
            articleList.append(GetRssFeedData(rssData))
        
