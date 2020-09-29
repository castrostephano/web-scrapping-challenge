from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain latest new title 
    content_title = soup.find_all('div', class_='content_title')
    link = content_title[1].find('a')
    news_title = link.get_text()

    # Retrieve all elements that contain corresponding paragraph text

    paragraph = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraph[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain latest new title 
    brand_title = soup.find_all('h2', class_='brand_title')

    # Output html of webpage
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # Store the url of the featured image
    featured_image_url = soup.find('a', class_="button fancybox")['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + str(featured_image_url)

    # Scrape from [Space Facts](https://space-facts.com/mars/)
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['description','value']
    df.set_index('description',inplace=True)
    mars_fact = df.to_html()

    # Scrape from USGS Astrogeology
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Output html of webpage
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    images = soup.find_all('div',class_='item')

    base_url = "https://astrogeology.usgs.gov"
    hemisphere_image_urls = []

    for image in images:
        # Find the hemisphere's url and title
        image_url = image.find('a',class_='itemLink product-item')['href']
        title = image.h3.text
        
        # Launch the hemisphere's url
        browser.visit(base_url + image_url)
        img = browser.html
        soup = BeautifulSoup(img,'html.parser')
        
        img_url = base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
        

    # Store data in a dictionary
    mars_data = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_fact" : mars_fact,
        "hemisphere_image_urls" : hemisphere_image_urls
    }     
        

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
