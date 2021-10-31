from RapidAPIFeed import GetRapidAPIFeed
from RssFeed import GetRssFeedUrls, GetRssFeedData
from json import dumps
from kafka import KafkaProducer
import time
rssSources=[
    {'name': 'TOI','homePage': 'https://timesofindia.indiatimes.com/',
    'rssPage': 'https://timesofindia.indiatimes.com/rss.cms','rssLinkFilter' : 'rssfeed'},
    {
    'name': 'NDTV','homePage': 'https://www.ndtv.com/',
    'rssPage': 'https://www.ndtv.com/rss','rssLinkFilter' : 'feedburner'}
    ]
queryStringList = ["Elon Musk","Bitcoin", "Rohit Sharma", "Harry Potter", "Egyptian Pyramids", "Covid", "Fifa", "Donald Trump", "Engineering", "Bank Robbery"]

def produceData(sourceType, sourceParams):
    producer = KafkaProducer(bootstrap_servers=['kafka:29092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

    if('rss' in sourceType.lower()):
        for rssSource in sourceParams:
            rssDataSet = GetRssFeedUrls(rssSource)
            for rssData in rssDataSet:
                producer.send(topic = "newsarticles", value = GetRssFeedData(rssData))

    elif('rapid' in sourceType.lower()):
        for queryString in sourceParams:
            articles = GetRapidAPIFeed(queryString)
            if(articles):
                producer.send(topic = "newsarticles", value = articles)

for t in range(10):
    # produceData('rss',rssSources)
    produceData('rapid',queryStringList)
    time.sleep(60)


