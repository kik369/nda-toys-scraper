from bs4 import BeautifulSoup
import requests
import json
import re
import time
from time import strftime

startTime = time.time()


with open('links.json', 'r') as jsonFile:
    allJsonUrls = json.load(jsonFile)

allItemInfo = []
singleItemInfo = {}
tags = []

for runIterator, url in enumerate(allJsonUrls):
    # print(f'Requesting... {url}')
    # Getting the webpage, creating a Response object.
    response = requests.get(url)

    # Extracting the source code of the page.
    data = response.text

    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, 'lxml')

    if soup.find("span", {"class": "thumbnail bannerButtonDiv"}) != None:
        productImageURL = soup.find(
            "span", {"class": "thumbnail bannerButtonDiv"}).find('img')['src']
    else:
        productImageURL = ''

    if soup.find('h3') != None:
        itemName = soup.find('h3').find('strong')
    else:
        itemName = ''

    # productCode = soup.findAll('td')[1]
    if 0 <= 1 < len(soup.findAll('td')):
        productCode = soup.findAll('td')[1]
    else:
        productCode = ''

    if 0 <= 1 < len(soup.findAll('td')):
        barCode = soup.findAll('td')[3]
    else:
        barCode = ''

    commodityCode = soup.findAll('td')[11]
    packSize = soup.find(string=re.compile("Pack Size"))
    rrp = soup.find(string=re.compile("RRP"))
    unitPrice = soup.find("span", {
                          "class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})[0]
    packPrice = soup.find("span", {
                          "class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})[1]

    singleItemInfo['productURL'] = url
    singleItemInfo['productImageURL'] = productImageURL
    singleItemInfo['itemName'] = itemName.text
    singleItemInfo['productCode'] = productCode.text
    singleItemInfo['barCode'] = barCode.text
    singleItemInfo['commodityCode'] = re.sub('\D', '', commodityCode.text)
    singleItemInfo['packSize'] = re.sub('\D', '', packSize.text)
    singleItemInfo['rrp'] = re.search('\d[.]\d*', rrp.text).group()
    singleItemInfo['unitPrice'] = re.search(
        '\d*[.]\d*', unitPrice.text).group()
    singleItemInfo['packPrice'] = re.search(
        '\d*[.]\d*', packPrice.text).group()

    if singleItemInfo not in tags:
        f''
        print(
            f'{runIterator + 1} of {len(allJsonUrls)} {round((runIterator + 1) / len(allJsonUrls) * 100, 2)}% {time.strftime("%H:%M:%S",  time.gmtime(time.time() - startTime))} {singleItemInfo["barCode"]} {singleItemInfo["productURL"]}')
        tags.append(singleItemInfo)
        singleItemInfo = {}

with open('details.json', 'w') as f:
    json.dump(tags, f)
