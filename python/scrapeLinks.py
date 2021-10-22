from bs4 import BeautifulSoup
import requests
import json
import time
from time import strftime

startTime = time.time()


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
        'https://www.nda-toys.com/251/wild-animal-toys-wholesale',
        'https://www.nda-toys.com/429/baby-alive-toys-wholesale',
        'https://www.nda-toys.com/159/barbie-wholesale',
        'https://www.nda-toys.com/548/bontempi-toys-wholesale',
        'https://www.nda-toys.com/160/ben-10-wholesale',
        'https://www.nda-toys.com/51/crayola-wholesale',
        'https://www.nda-toys.com/412/dc-comics-toys-wholesale',
        'https://www.nda-toys.com/164/disney-toys-wholesale',
        'https://www.nda-toys.com/625/fisher-price-wholesale',
        'https://www.nda-toys.com/62/fun-craft-wholesale',
        'https://www.nda-toys.com/64/fun-stationery-wholesale',
        'https://www.nda-toys.com/67/fun-toys-wholesale',
        'https://www.nda-toys.com/489/gelli-baff-toys-wholesale',
        'https://www.nda-toys.com/657/harry-potter-wholesale',
        'https://www.nda-toys.com/81/hasbro-gaming-wholesale',
        'https://www.nda-toys.com/695/hot-wheels-wholesale',
        'https://www.nda-toys.com/721/imaginext-wholesale',
        'https://www.nda-toys.com/88/jokes-and-gags-toys-wholesale',
        'https://www.nda-toys.com/611/knex-wholesale',
        'https://www.nda-toys.com/585/little-live-pets-wholesale',
        'https://www.nda-toys.com/174/marvel-toys-wholesale',
        'https://www.nda-toys.com/694/mattel-games-wholesale',
        'https://www.nda-toys.com/696/mega-bloks-wholesale',
        'https://www.nda-toys.com/229/my-little-pony-toys-wholesale',
        'https://www.nda-toys.com/4/nerf-wholesale',
        'https://www.nda-toys.com/508/paint-glow-wholesale',
        'https://www.nda-toys.com/231/paw-patrol-toys-wholesale',
        'https://www.nda-toys.com/7/peppa-pig-wholesale',
        'https://www.nda-toys.com/449/pikmi-pops-toys-wholesale',
        'https://www.nda-toys.com/277/pj-mask-toys-wholesale',
        'https://www.nda-toys.com/116/play-doh-wholesale',
        'https://www.nda-toys.com/118/playskool-toys-wholesale',
        'https://www.nda-toys.com/232/pokemon-toys-wholesale',
        'https://www.nda-toys.com/437/schleich-wholesale',
        'https://www.nda-toys.com/236/shopkins-toys-wholesale',
        'https://www.nda-toys.com/476/spirograph-toys-wholesale',
        'https://www.nda-toys.com/433/stickle-bricks-wholesale',
        'https://www.nda-toys.com/134/teamsterz-toys-wholesale',
        'https://www.nda-toys.com/241/thomas-and-friends-toys-wholesale',
        'https://www.nda-toys.com/215/toy-story-toys-wholesale',
        'https://www.nda-toys.com/242/transformers-toys-wholesale',
        'https://www.nda-toys.com/245/wwe-toys-wholesale',
        'https://www.nda-toys.com/704/xootz-wholesale'
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
            print(
                f'{time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))} Adding... {pageTag.get("href")}')
            all_links.append(pageTag.get('href'))

        elif 'page=' in str(pageTag.get('href')) and pageTag.get('href') not in all_page_links:
            print(f'Page link... {pageTag.get("href")}')
            all_page_links.append(pageTag.get('href'))
            add_links_to_list(pageTag.get('href'))


for url in urls:
    add_links_to_list(url)

with open('links.json', 'w') as f:
    json.dump(all_links, f)

print(f'{len(all_links)} links found in {time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))}')
