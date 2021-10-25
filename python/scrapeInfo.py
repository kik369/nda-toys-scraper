from os import error
from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
import re


def getProductInfo():
    startTime = time.time()

    with open('links.json', 'r') as jsonFile:
        allJsonUrls = json.load(jsonFile)

    singleItemInfo = {}
    tags = []

    for runIterator, url in enumerate(allJsonUrls):
        try:
            response = requests.get(url)

            data = response.text

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

            if 1 < len(soup.findAll('td')):
                productCode = soup.findAll('td')[1]
            else:
                productCode = ''

            if 3 < len(soup.findAll('td')):
                barCode = soup.findAll('td')[3]
            else:
                barCode = ''

            if 11 < len(soup.findAll('td')):
                commodityCode = soup.findAll('td')[11]
            else:
                commodityCode = ''

            packSize = soup.find(string=re.compile("Pack Size"))

            rrp = soup.find(string=re.compile("RRP"))

            unitPrice = soup.find("span", {
                "class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})
            if 0 < len(unitPrice):
                unitPrice = soup.find("span", {
                    "class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})[0]
            else:
                unitPrice = ''

            packPrice = soup.find("span", {
                "class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})
            if 1 < len(packPrice):
                packPrice = soup.find(
                    "span", {"class": "col-xs-12 col-md-3 col-lg-3"}).findAll("span", {"class": "highlight"})[1]
            else:
                packPrice = ''

            singleItemInfo['productURL'] = url
            singleItemInfo['productImageURL'] = productImageURL
            singleItemInfo['itemName'] = itemName.text
            singleItemInfo['productCode'] = productCode.text
            singleItemInfo['barCode'] = barCode.text
            singleItemInfo['commodityCode'] = re.sub(
                '\D', '', commodityCode.text)
            singleItemInfo['packSize'] = re.sub('\D', '', packSize.text)
            singleItemInfo['rrp'] = re.search('\d*[.]\d*', rrp.text).group()
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
        except:
            print(f'Error {error}')

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    with open(f'output/product-data/json/info-nda-toys-{fileNameTimeStamp}.json', 'w') as f:
        json.dump(tags, f)
