from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

#Mars news site
def mars_news():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    browser.is_element_present_by_css("ul.item_list li.slide")
    html = browser.html
    nsoup = BeautifulSoup(html, "html.parser")

    try:


#JPL featured images






    browser.quit()

    return listings