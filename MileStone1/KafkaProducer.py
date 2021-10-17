from RapidAPIFeed import GetRapidAPIFeed
from RssFeed import GetRssFeedUrls, GetRssFeedData
from json import dumps
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
rssSources=[
    {'name': 'TOI','homePage': 'https://timesofindia.indiatimes.com/',
    'rssPage': 'https://timesofindia.indiatimes.com/rss.cms','rssLinkFilter' : 'rssfeed'},
    {
    'name': 'NDTV','homePage': 'https://www.ndtv.com/',
    'rssPage': 'https://www.ndtv.com/rss','rssLinkFilter' : 'feedburner'}
    ]
for rssSource in rssSources:
        rssDataSet = GetRssFeedUrls(rssSource)
        for rssData in rssDataSet:
            producer.send(topic = "newsarticles", value = GetRssFeedData(rssData))

queryStringList = ["Elon Musk","Bitcoin", "Rohit Sharma", "Harry Potter", "Egyptian Pyramids", "Covid", "Fifa", "Donald Trump", "Engineering", "Bank Robbery"]
for queryString in queryStringList:
    articles = GetRapidAPIFeed(queryString)
    if(articles):
        producer.send(topic = "newsarticles", value = articles)

    
# rssArticles = GetRssData(rssSources)
# rapidAPIArticles = GetRapidAPIData(queryStringList)
# InjectToMongodb(rssArticles)
# InjectToMongodb(rapidAPIArticles)