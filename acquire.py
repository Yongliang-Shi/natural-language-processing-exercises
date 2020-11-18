import numpy as np
import pandas as pd

from requests import get
import re
from bs4 import BeautifulSoup

import os

# %%
def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object
    '''
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# %%
def get_blog_urls():
    '''
    This function scrapes all of the Codeup blog urls from the main Codeup blog page
    Returning a list of urls
    '''
    base_url = 'https://codeup.com/resources/#blog' 
    soup = make_soup(base_url)
    urls_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    urls = {url.get('href') for url in urls_list}
    urls = list(urls)
    return urls

# %%
def acquire_codeup_blogs(urls, cached=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter with default cashed == False.
    It scrapes the title and text for each url, creates a list of dictionaries with title and tex for each blog,
    creates a list of dictionaries, converts list to df, and returns df
    If cached == True, the function returns a dataframe from a json file.     
    '''
    if cached == True:
        df = pd.read_json('codeup_blogs.json') # cached == False completes a fresh scrape for df. 
    else:
        
        blog_articles = []
        
        for url in urls:
            soup = make_soup(url)
            title = soup.find('h1', class_='jupiterx-post-title')
            content = soup.find('div', class_='jupiterx-post-content')
            d = {'title': title.text, 'original': content.text}
            blog_articles.append(d)
        
        df = pd.DataFrame(blog_articles)
        df.to_json('codeup_blogs.json')
    return df

# %%
def get_news_articles(cached=False):
    '''
    This function with default cached == False does a fresh  scrape of inshorts pages with topics business, sports, technology, 
    and entertainment and writes the returned df to a json file. 
    cached == True returns a df read in from a json file. 
    '''
    if cached == True:
        df = pd.read_json('inhorts_articles.json')
    else:
        base_url = 'https://inshorts.com/en/read/'
        topics = ['business', 'sports', 'technology', 'entertainment']
        articles = []
        for topic in topics:
            topic_url = base_url + topic
            soup = make_soup(topic_url)
            cards = soup.find_all('div', class_='news-card')
            for card in cards:
                title = card.find('span', itemprop = 'headline').text
                author = card.find('span', class_ = 'author').text
                content = card.find('div', itemprop = 'articleBody').text
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'original': content})
                articles.append(article)
        df = pd.DataFrame(articles)
        df.to_json('inhorts_articles.json')
    return df