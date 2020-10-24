import feedparser
import csv
import pandas as pd
import re

newsurls = {
    'Yandex.News': 'https://news.yandex.ru/koronavirus.rss'
}  # пример словаря RSS-лент

f_all_news = 'allnews23march.csv'
f_certain_news = 'certainnews23march.csv'

vector1 = ' '  # пример таргетов
vector2 = ' '


def parseRSS(rss_url):  # функция получает линк на рсс ленту, возвращает распаршенную ленту с помощью feedpaeser
    return feedparser.parse(rss_url)


def getHeadlines(rss_url):  # функция для получения заголовков новости
    headlines = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines


def getDescriptions(rss_url):  # функция для получения описания новости
    descriptions = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        descriptions.append(newsitem['description'])
    return descriptions


def getLinks(rss_url):  # функция для получения ссылки на источник новости
    links = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        links.append(newsitem['link'])
    return links


def getDates(rss_url):  # функция для получения даты публикации новости
    dates = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        dates.append(newsitem['published'])
    return dates


allheadlines = []
alldescriptions = []
alllinks = []
alldates = []
# Прогоняем нашии URL и добавляем их в наши пустые списки
for key, url in newsurls.items():
    allheadlines.extend(getHeadlines(url))

for key, url in newsurls.items():
    alldescriptions.extend(getDescriptions(url))

for key, url in newsurls.items():
    alllinks.extend(getLinks(url))

for key, url in newsurls.items():
    alldates.extend(getDates(url))


def write_all_news(all_news_filepath):  # функция для записи всех новостей в .csv, возвращает нам этот датасет
    header = ['Title', 'Description', 'Links', 'Publication Date']

    with open(all_news_filepath, 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerow(i for i in header)

        for a, b, c, d in zip(allheadlines, alldescriptions,
                              alllinks, alldates):
            writer.writerow((a, b, c, d))

        df = pd.read_csv(all_news_filepath)

    return df


def looking_for_certain_news(all_news_filepath, certain_news_filepath, target1, target2):
    df = pd.read_csv(all_news_filepath)

    result = df.apply(lambda x: x.str.contains(target1, na=False,
                                               flags=re.IGNORECASE, regex=True)).any(axis=1)
    result2 = df.apply(lambda x: x.str.contains(target2, na=False,
                                                flags=re.IGNORECASE, regex=True)).any(axis=1)
    new_df = df[result & result2]

    new_df.to_csv(certain_news_filepath
                  , sep='\t', encoding='utf-8-sig')

    return new_df


write_all_news(f_all_news) #все новости


looking_for_certain_news(f_all_news, f_certain_news, vector1, vector2)  # новости по вектору


with open('certainnews23march.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    c = 0
    news = {}
    for row in reader:
        strw = ""
        for i in row:
            strw = strw + str(i)
        hgdsfh = strw.replace('&quot;', '').split('\t')
        news[c] = ([hgdsfh[1], hgdsfh[3]])
        c += 1
print(news[1][0])
print(news[1][1])




