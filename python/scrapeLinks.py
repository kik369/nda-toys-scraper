from os import error
from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
from scrapeInfo import getProductInfo
from jsonToCsv import jsonToCsv

startTime = time.time()

url = 'https://www.nda-toys.com/'

all_product_links = set()
all_page_links = set()
all_links = set()


def crawler(url):
    all_links.add(url)
    print(
        f'{time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Checking... {url}')

    try:
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        pageTags = soup.find_all("a")

        for pageTag in pageTags:
            tag = str(pageTag.get('href'))
            if tag not in all_product_links and 'https://www.nda-toys.com/product/' in tag:
                print(f'Adding... {tag}')
                all_product_links.add(tag)
                all_links.add(tag)

            elif 'page=' in tag and tag not in all_page_links:
                print(f'Page... {tag}')
                all_page_links.add(tag)
                # all_links.add(tag)
                crawler(tag)

            elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
                all_links.add(tag)
                crawler(tag)

    except:
        print(f'{error} in url {url}, tag {tag}')


def scrapeWebsite():

    global all_product_links, all_page_links, all_links

    crawler(url)

    all_product_links = list(all_product_links)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    with open(f'output/link-data/links-nda-toys-{fileNameTimeStamp}.json', 'w') as f:
        json.dump(all_product_links, f)

    print(f'Products: {len(all_product_links)}. Pages: {len(all_page_links)}. URLs checked: {len(all_links)} in {time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))}')


scrapeWebsite()

getProductInfo()

jsonToCsv()

# datetime.datetime.now().strftime('%H:%M')
# datetime.datetime.now().isoformat()

# I think the following is the best one
# datetime.datetime.utcnow().isoformat()
# '2021-10-23T10:46:36.291865'

# datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')

# tzinfo=datetime.timezone.utc)
# datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
