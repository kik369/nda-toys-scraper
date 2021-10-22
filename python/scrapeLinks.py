from os import error
from bs4 import BeautifulSoup
import requests
import json
import time

startTime = time.time()

url = 'https://www.nda-toys.com/'

all_product_links = set()
all_page_links = set()
all_links = set()


def add_links_to_list(url):
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
                print(
                    f'Adding... {tag}')
                all_product_links.add(tag)
                all_links.add(tag)

            elif 'page=' in tag and tag not in all_page_links:
                print(f'Page... {tag}')
                all_page_links.add(tag)
                all_links.add(tag)
                add_links_to_list(tag)

            elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
                all_links.add(tag)
                add_links_to_list(tag)

    except:
        print(f'{error} in url {url}, tag {tag}')


add_links_to_list(url)

all_product_links = list(all_product_links)

with open('links.json', 'w') as f:
    json.dump(all_product_links, f)

print(f'Products: {len(all_product_links)}. Pages: {len(all_page_links)}. URLs checked: {len(all_links)} in {time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))}')
