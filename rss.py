from os import write
import requests
from bs4 import BeautifulSoup

#This is a fail-safe to make sure I get responses from my scraping. If I don't open a page or if there is a time-out, I exit and move to the next url
def fetch_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    page = requests.get(url.rstrip(),headers = headers)
    return page

head="""
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Redlands Orange Press</title>
    <meta name="description" content="A site for you to find events, businesses, gyms, community in Redlands for people moving to or living in Redlands, California.">
    <link rel="stylesheet" href="http://redlandsorangepress.com/extension.css">
    <link rel="apple-touch-icon" sizes="180x180" href="img/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="img/favicon-16x16.png">
    <link rel="manifest" href="img/site.webmanifest">
</head>
<body>
<h1 id="header">Redlands Orange Press</h1>
<section>
    <section style="width:50%;float:left;display:block;text-align: center;">
        <a href="https://redlandsorangepress.com" ><h2>Community events</h2></a>
    </section>    
    <section style="width:50%;float:right;display:block;text-align: center;">
        <a href="https://redlandsorangepress.com/news"><h2 style="text-color:black">Morning news</h2></a>
    </section>  
</section>    
<section>
<img class="partnerwordmark" alt="Community Forward Redlands" src="https://www.communityforwardredlands.com/content/images/2024/01/CFR-logo_Website-Header--1-.png">

"""

article_sections=   """<article class_="articlephototop">
    <div class_="storyphoto">
    <a href="{link_}" target="_top">
      <img class="article_photo" style="background-image:url({photo_});"/>
      <h3>{headline_}</h3> </a>
    </div>

  </article>"""

calmatters_interlude="""
<br><br>
            <img style="padding-top:20px; padding-bottom:20px" decoding="async" alt="CalMatters" src="https://i0.wp.com/calmatters.org/wp-content/uploads/2019/07/calmatters-logo_2x.png?fit=488%2C82&amp;ssl=1" class="i-amphtml-fill-content i-amphtml-replaced-content">
<br><br>


"""

rdf_interlude="""
<br><br>
            <img style="padding-top:20px; padding-bottom:20px" decoding="async" alt="Redlands Daily Facts logo" src="https://www.redlandsdailyfacts.com/wp-content/uploads/2017/08/redlands-main-logo.svg" class="i-amphtml-fill-content i-amphtml-replaced-content">
<br><br>


"""

lat_interlude="""
<br><br>
            <img style="padding-top:20px; padding-bottom:20px" decoding="async" alt="Redlands Daily Facts logo" src="https://upload.wikimedia.org/wikipedia/commons/b/be/Los_Angeles_Times.svg" class="i-amphtml-fill-content i-amphtml-replaced-content">
<br><br>


"""

end="""</section>
</body>
</html>
""" 

def find_story_info(item):
    headline=item.find("title").get_text()
    link=item.find("link").get_text()
    if item.find("media:content"):
        photo=item.find("media:content")['url']
    else:
        return(headline,link,"no photo")
    return(headline,link,photo)

def grab_info_redlands(html):
    count=0
    page=fetch_page("https://www.communityforwardredlands.com/rss/")
    if not page: 
        return
    soup=BeautifulSoup(page.content,"html.parser")
    for item in soup.find_all("item"):
        headline,link,photo=find_story_info(item)
        if photo == "no photo":
            continue
        new_article_section=article_sections.format(link_=link,photo_=photo,headline_=headline)
        html=html+new_article_section
        count+=1
        if count==6:
            return(html)
    return(html)

def grab_info_rdf(html):
    count=0
    page=fetch_page("https://www.redlandsdailyfacts.com/location/california/los-angeles-county/inland-empire/redlands/feed/")
    if not page: 
        return
    soup=BeautifulSoup(page.content,"html.parser")
    for item in soup.find_all("item"):
        print("####")
        headline,link,photo=find_story_info(item)
        print(headline)
        print(link)
        if photo == "no photo":
            continue
        new_article_section=article_sections.format(link_=link,photo_=photo,headline_=headline)
        html=html+new_article_section
        count+=1
        if count==6:
            return(html)
    return(html)

def find_story_info_calmatters(item):
    skip="skip"
    accepted_categories=["Politics","California Legislature","Capitol","California Governor","Education","Higher Education"]
    if item.find("category"):
        for category in item.find_all("category"):
            if category.get_text()in accepted_categories:
                skip="Don't skip"
    if skip=="skip":
        return("headline","link","no photo")
    headline=item.find("title").get_text()
    link=item.find("link").get_text()
    if item.find("thumbnail"):
        photo=item.find("thumbnail")['url'].split("?")[0]
    else:
        return(headline,link,"no photo")
    return(headline,link,photo)

def grab_info_calmatters(html):
    count=0
    page=fetch_page("https://calmatters.org/feed/?partner-feed=aidan")
    if not page: 
        return
    soup=BeautifulSoup(page.content,"html.parser")
    for item in soup.find_all("item"):
        headline,link,photo=find_story_info_calmatters(item)
        if photo == "no photo":
            continue
        new_article_section=article_sections.format(link_=link,photo_=photo,headline_=headline)
        html=html+new_article_section
        count+=1
        if count==6:
            return(html)
    return(html)

def grab_info_lat(html):
    count=0
    page=fetch_page("https://www.latimes.com/california/rss2.0.xml#nt=0000016c-0bf3-d57d-afed-2fff84fd0000-1col-7030col1")
    if not page: 
        return
    soup=BeautifulSoup(page.content,"html.parser")
    for item in soup.find_all("item"):
        headline,link,photo=find_story_info(item)
        if photo == "no photo":
            continue
        new_article_section=article_sections.format(link_=link,photo_=photo,headline_=headline)
        html=html+new_article_section
        count+=1
        if count==6:
            return(html)
    return(html)

        
def grab_info():
    html=head
    html=grab_info_redlands(html)
    html=html+rdf_interlude
    html=grab_info_rdf(html)
    html=html+calmatters_interlude
    html=grab_info_calmatters(html)
    html=html+lat_interlude
    html=grab_info_lat(html)
    html=html+end
    with open("news.html","w") as f:
        f.write(html)
        
grab_info()
