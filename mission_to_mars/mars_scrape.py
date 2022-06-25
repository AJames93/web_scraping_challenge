from bs4 import BeautifulSoup as bs
import pymongo
import requests
from splinter import Browser
import os
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

#database 
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {'executable_path': 'chromedriver.exe'}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    collection.drop()

#news on mars
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    mars_html = browser.html
    mars_news = bs(mars_html,'lxml')
    try:
        news_title = mars_news.find("div",class_="content_title").text
        news_paragraph = mars_news.find("div", class_="article_teaser_body").text
    except AttributeError:
        return None, None
#mars images 
    jurl = 'https://www.spaceimages-mars.com/'
    browser.visit(jurl)
    button = browser.find_by_tag('button')[1]
    button.click()
    jhtml = browser.html
    jpl_soup = bs(jhtml,"html.parser")
    # image_url = jpl_soup.find('div',class_='fancybox-image"').article.footer.a['data-fancybox-href']
    # try:
    feat_img = jpl_soup.find("img", class_="fancybox-image").get("src")
    # except AttributeError:
#     return None
# print(jurl+ft_img)
    # base_link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    feature_url = jurl+ft_img
    # featured_image_title = jpl_soup.find('h1', class_="media_feature_title").text.strip()

#facts on mars 
    facts_url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(facts_url)
    m_df = table[0]
    m_df = mars_df.rename(columns={0: "Mars - Earth Comparison", 1: "Mars", 2: "Earth"})
    m_df = mars_df.drop(0)
    m_df =  mars_df[['Mars - Earth Comparison', 'Mars']]
    m_facts_html = mars_df.to_html(header=False, index=False)
    m_facts_html.replace("\n", "")

#mars hemis 
    m_hemi_url = 'https://www.marshemispheres.com/'
    browser.visit(m_hemi_url)  
    m_hemi_html = browser.html 
    m_hemi_soup = bs(m_hemi_html,"html.parser") 
    results = m_hemi_soup.find_all("div",class_='item')
    m_hemi_image_urls = []
    for result in results:
            product_dict = {}
            titles = result.find('h3').text
            end_link = result.find("a")["href"]
            image_link = "https://www.marshemispheres.com/" + end_link    
            browser.visit(image_link)
            html = browser.html
            soup= bs(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.find("a")["href"]
            product_dict['title']= titles
            product_dict['image_url']= mhurl+image_url
            m_hemi_image_urls.append(product_dict)

#close the browser
    browser.quit()

    #results
    mars_data ={
		'news_title' : news_title,
		'summary': news_paragraph,
        'featured_image': feature_url,
		'fact_table': m_facts_html,
		'hemisphere_image_urls': m_hemi_image_urls,
        'news_url': news_url,
        'jpl_url': jurl,
        'fact_url': facts_url,
        'hemisphere_url': m_hemi_url,
        }
    collection.update_one({},{"$set":mars_data},upsert=True)
    print(m_hemi_image_urls)