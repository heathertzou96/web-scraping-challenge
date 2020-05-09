from bs4 import BeautifulSoup
import requests
import os
import re
import time 
import pandas as pd
from splinter import Browser

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False) 

def scrape():

    all_scraped_data = {}

    all_news = mars_news()
    all_scraped_data["title"] = all_news[0]
    all_scraped_data["paragraph"] = all_news[1]

    all_scraped_data["images"] = mars_images()

    all_scraped_data["weather"] = mars_weather()
    
    all_scraped_data["facts"] = mars_facts()

    all_scraped_data["hemispheres"] = mars_hemispheres()

    return(all_scraped_data)


def mars_news():

    news_url ="https://mars.nasa.gov/news/"
    browser.visit(news_url)

    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    article = soup.find('div', class_='list_text')
    title = article.find('div', class_='content_title').text
    
    paragraph = soup.find('div', class_= 'article_teaser_body').text

    news = [title, paragraph]
    
    return news

def mars_images():

    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url) 

    fullimage_button = browser.find_by_id('full_image')
    fullimage_button.click() 
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")   
    
    figure = soup.find('figure', class_='lede')
    image_url = figure.a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    return featured_image_url


def mars_weather():

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url) 

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        mars_weather = soup.find("p", "tweet-text").get_text()
    except:
        pattern = re.compile(r'InSight') 
        mars_weather = soup.find('span', text=pattern).text
    
    return mars_weather


def mars_facts():

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url) 
    
    tables = pd.read_html(facts_url)
    
    table = pd.DataFrame(tables[0])
    table.columns = ['Mars Info', 'Values']
    table = table.set_index('Mars Info')
    mars_table = table.to_html()

    return mars_table


def mars_hemispheres():

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all('div', class_='item')

    base_url = "https://astrogeology.usgs.gov"

    hemisphere_image_urls = []

    for item in items:
        href = item.find('a').get('href')
        
        title = item.find('h3').text
        title = title.replace('Enhanced', '')
        
        hemisphere_page = base_url + href
        browser.visit(hemisphere_page)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        download = soup.find('div', class_ = 'downloads')
        img_url = download.find('a')['href']
        
        mars_dict = {"title": title, "img_url": img_url}
        hemisphere_image_urls.append(mars_dict)
    
    return hemisphere_image_urls

    