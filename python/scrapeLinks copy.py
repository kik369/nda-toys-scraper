from bs4 import BeautifulSoup
import requests
import json


urls = ['https://www.nda-toys.com/13/toys-wholesale',
'https://www.nda-toys.com/16/arts-and-crafts-wholesale',
'https://www.nda-toys.com/15/stationery-wholesale',
'https://www.nda-toys.com/14/books-wholesale',
'https://www.nda-toys.com/372/party-supplies-wholesale',
'https://www.nda-toys.com/latest-additions',
'https://www.nda-toys.com/coming-soon',
'https://www.nda-toys.com/wholesale-toy-deals',
'https://www.nda-toys.com/247/alien-wholesale',
'https://www.nda-toys.com/34/dinosaurs-wholesale',
'https://www.nda-toys.com/249/fairies-and-princesses-wholesale',
'https://www.nda-toys.com/250/farm-toys-wholesale',
'https://www.nda-toys.com/260/fire-brigade-toys-wholesale',
'https://www.nda-toys.com/261/football-toys-wholesale',
'https://www.nda-toys.com/248/super-hero-wholesale',
'https://www.nda-toys.com/583/unicorn-wholesale',
'https://www.nda-toys.com/251/wild-animal-toys-wholesale'
]

all_links = []
all_page_links = []


def add_links_to_list(url):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    pageTags = soup.find_all("a")

    for pageTag in pageTags:
        if pageTag.get('href') not in all_links and str(pageTag.get('href'))[0:33] == 'https://www.nda-toys.com/product/':
            print(f'Adding... {pageTag.get("href")}')
            all_links.append(pageTag.get('href'))

        if 'page=' in str(pageTag.get('href')) and pageTag.get('href') not in all_page_links:
            print(f'Page link... {pageTag.get("href")}')
            all_page_links.append(pageTag.get('href'))
            add_links_to_list(pageTag.get('href'))

    # for link in all_page_links:
    #     print(link)
    
    # json_string = json.dumps(all_page_links)
    with open('links.json', 'w') as f:
        json.dump(all_links, f)

    print(f'{len(all_links)} links found')


for url in urls:
    add_links_to_list(url)
