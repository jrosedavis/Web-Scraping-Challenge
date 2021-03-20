from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

mongo_conn='mongodb://localhost:27017'
client=pymongo.MongoClient(mongo_conn)

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)
    return browser

def scrape_info():
    browser = init_browser()

    #Mars news
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    time.sleep(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_="rollover_description_inner").text

    #JPL featured image

    img_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(1)

    browser.find_by_css('img.BaseImage').click()
    
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    featured_image = img_soup.find_all('img', class_='BaseImage')[3]['src']
    featured_img_url = featured_image

    #Mars facts (used pandas)

    mars_facts_url = 'https://space-facts.com/mars/'
    table_list = pd.read_html(mars_facts_url)
    mars_df = table_list[0]
    mars_df.columns = ['Mars Planet Profile', 'Facts']
    clean_mars = mars_df.drop(0)
    cleaner_mars = clean_mars.set_index('Mars Planet Profile')
    mars_facts = cleaner_mars.to_html(index=True)

    #Mars hemispheres

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html

    hemis_soup = BeautifulSoup(html, 'html.parser')
    hemis_items = soup.find_all('div', class_='downloads')

    img_urls = []
    main_hemis_url = 'https://astrogeology.usgs.gov'

    for x in range(4):
        html = browser.find_by_css('.thumb')[x].click() #tried css also

        img_html = browser.html
        hemis_soup = BeautifulSoup(img_html, 'html.parser')

        full_img_url = hemis_soup.find('img', class_='wide-image')['src']
        fin_url = main_hemis_url + full_img_url

        title = browser.find_by_css('.title').text

        img_urls.append({'title': title,
                         'img_ur': fin_url})
    
    browser.back()
    browser.quit()

#Create a scrape function via a dictionary

    mars_data = {"news_title": news_title,
                "news_p": news_p,
                "featured_image_url": featured_img_url,
                "mars_facts": mars_facts,
                "hemispheres": img_urls}

    browser.quit()

    return mars_data
