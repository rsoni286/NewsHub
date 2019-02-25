import urllib3
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/news", methods=['GET'])
def get_news():
    cc = request.args['cc']
    if cc == 'np':
        http = urllib3.PoolManager()
        link = 'https://thehimalayantimes.com/'
        page = http.request('GET', link)
        soup = BeautifulSoup(page.data, features="html.parser")
        news = soup.find('ul', attrs={'class': "mainNews"})
        head = news.find_all('li')
        res = []
        for a in head:
            h1 = a.find('h4')
            headline = h1.text.strip()
            link = h1.find('a')['href']
            img_div = a.find('div', attrs={'class': 'wp-caption alignleft'})
            img_link = img_div.find('img')['data-medium-file']
            desc = a.find('p').text.strip()
            b = {"headline": headline, "desc": desc, "link": link, 'img_link': img_link}
            res.append(b)

        return render_template("newsfeed.html", res=res, cc=cc)
    elif cc == 'in' or cc == 'us' or cc == 'br' or cc == 'au':

        url = "https://newsapi.org/v2/top-headlines?country=" + cc + "&apiKey=9ef5d3d7dc7e428a8d93c15ccbfdc092&pageSize=5"
        response = requests.get(url)
        data = response.json()
        size=data['totalResults']
        if size >0:
            news_list = data["articles"]
            res=[]
            for a in news_list:
                headline=a['title']
                desc = a['description']
                link = a['url']
                img_link=a['urlToImage']
                b = {"headline": headline, "desc": desc, "link": link, 'img_link': img_link}
                res.append(b)

            return render_template("newsfeed.html",res=res,cc=cc)
        else:
            res = [{"headline": "Nothing to show", "desc": "", "link": "", 'img_link': ""}]
            return render_template("newsfeed.html",res=res,cc="")

    else:
        res = [{"headline": "Nothing to show", "desc": "", "link": "", 'img_link': ""}]
        return render_template("newsfeed.html", res=res, cc="")


if __name__ == "__main__":
    app.run(debug=True)
