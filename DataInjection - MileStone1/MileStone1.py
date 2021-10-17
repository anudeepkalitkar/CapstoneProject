from mongoInjection import InjectToMongodb
from RapidAPIFeed import GetRapidAPIData
from RssFeed import GetRssData



queryStringList = ["Elon Musk","Bitcoin", "Rohit Sharma", "Harry Potter", "Egyptian Pyramids", "Covid", "Fifa", "Donald Trump", "Engineering", "Bank Robbery"]
rssSources=[
    {'name': 'TOI','homePage': 'https://timesofindia.indiatimes.com/',
    'rssPage': 'https://timesofindia.indiatimes.com/rss.cms','rssLinkFilter' : 'rssfeed'},
    {
    'name': 'NDTV','homePage': 'https://www.ndtv.com/',
    'rssPage': 'https://www.ndtv.com/rss','rssLinkFilter' : 'feedburner'}
    ]
rssArticles = GetRssData(rssSources)
rapidAPIArticles = GetRapidAPIData(queryStringList)
InjectToMongodb(rssArticles)
InjectToMongodb(rapidAPIArticles)
    