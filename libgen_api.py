import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify
app = Flask(__name__)

def make_request(req):
    url = "https://libgen.rs/search.php?req="
    res = requests.get(url+req)
    return res

def get_download_urls(search_query):
    html_data = make_request(search_query)
    soup = BeautifulSoup(html_data.content, 'html5lib')
    links = []
    a_tags = soup.find_all('a')
    download_data = []

    for tag in a_tags:
        if tag.string == "[1]":
            links.append(tag.get("href"))
    #print(links)
    
    for link in links:
        response = BeautifulSoup(requests.get(link).content, 'html5lib')
        title = response.find('h1').string
        urls = response.find_all('a')
        libgen_link,cloudflare_link = "",""
        info = []
        for tag in urls:
            if tag.string == "GET":
                libgen_link = tag.get("href")
            if tag.string == "Cloudflare":
                cloudflare_link = tag.get("href")
        p_tags = response.find_all(lambda tag:tag.name == 'p' and not tag.attrs)

        for tag in p_tags:
            info.append(tag.string)
        download_data.append([title,libgen_link,cloudflare_link,info])
    #print(download_data)
    return download_data
        

@app.route('/get-book/<keyword>')
def get_book(keyword):
     data = get_download_urls(keyword)
     return jsonify({"data":data})
    

