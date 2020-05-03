from bs4 import BeautifulSoup
import requests
import os
import re
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

    all_scraped_data["hemispheres"] = mars_hemispheres

    return(all_scraped_data)


def mars_news():

    url ="https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    news_title = soup.find('div', class_= 'content_title').text.strip()
    news_p = soup.find('div', class_= 'rollover_description_inner').text.strip()

    news = [news_title, news_p]

    return news


def mars_images():

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url) 

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

    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 

    tweet = soup.find_all('div', class_="js-tweet-text-container")[0]
    for p in tweet.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        mars_weather = p.text
    
    return mars_weather


def mars_facts():

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Mars Info', 'Values']
    df.set_index('Mars Info', inplace = True)

    html_table = df.to_html()
    html_table = html_table.replace('\n','')
    
    return html_table


def mars_hemispheres():

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

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
        html_2 = browser.html
        soup = BeautifulSoup(html_2, "html.parser")
        
        download = soup.find('div', class_ = 'downloads')
        img_url = download.find('a')['href']
        
        dict = {"title": title, "img_url": img_url}
        hemisphere_image_urls.append(dict)
    
    return hemisphere_image_urls

    