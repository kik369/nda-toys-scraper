import csv
import datetime
import json
import logging
import re
import requests
from bs4 import BeautifulSoup


def currentTime():
    return datetime.datetime.today().strftime('%Y/%m/%d @ %H:%M:%S')


fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d')
logFile = f'output/logs/log-{fileNameTimeStamp}.log'
open(logFile, 'w')
logging.basicConfig(filename=logFile, level=logging.INFO)

logging.info(f'{currentTime()} SEARCHING FOR PRODUCTS')

url = 'https://www.nda-toys.com/'

all_product_links = set()
all_page_links = set()
all_links = set()


def crawler(url):
    all_links.add(url)
    logging.info(
        f'{currentTime()} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Checking... {url}')

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    pageTags = soup.find_all('a')

    for pageTag in pageTags:
        tag = str(pageTag.get('href'))
        if tag not in all_product_links and 'https://www.nda-toys.com/product/' in tag:
            all_product_links.add(tag)
            all_links.add(tag)
            logging.info(
                f'{currentTime()} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Product link... {tag}')

        elif 'page=' in tag and tag not in all_page_links:
            all_page_links.add(tag)
            all_links.add(tag)
            logging.info(
                f'{currentTime()} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | New page... {tag}')

            crawler(tag)

        elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
            all_links.add(tag)
            crawler(tag)

    return all_product_links


def writeProductLinksToJson(all_product_links):

    logging.info(
        f'{currentTime()} WRITING PRODUCT LINKS TO JSON')

    all_product_links = list(all_product_links)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileName = f'links-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/link-data/{fileName}', 'w') as f:
        json.dump(all_product_links, f)

    logging.info(
        f'{currentTime()} Succesfullt written {len(all_product_links)} product links to JSON')

    return fileName


def toInt(string):
    if string != None:

        string = re.sub('\D', '', string)

        if string != '':
            string = int(string)

    return string


def toFloat(string):
    if string != None:
        string = re.search('\d*[.]\d*', string.text).group()
        string = '{:.2f}'.format(float(string))

    return string


def getProductInfo(fileName):

    logging.info(
        f'{currentTime()} GETTING PRODUCT INFO')

    fPath = f'output/link-data/{fileName}'

    with open(fPath, 'r') as jsonFile:
        allJsonUrls = json.load(jsonFile)

    singleItemInfo = {}
    tags = []

    for runIterator, url in enumerate(allJsonUrls):
        response = requests.get(url)

        data = response.text

        soup = BeautifulSoup(data, 'lxml')

        if soup.find('span', {'class': 'thumbnail bannerButtonDiv'}) != None:
            imageURL = soup.find(
                'span', {'class': 'thumbnail bannerButtonDiv'}).find('img')['src']
        else:
            imageURL = ''

        if soup.find('h3').find('strong') != None:
            itemName = soup.find('h3').find('strong').text
        else:
            itemName = ''

        if 1 < len(soup.findAll('td')):
            productCode = soup.findAll('td')[1].text
            productCode = toInt(productCode)

        if 3 < len(soup.findAll('td')):
            barCode = soup.findAll('td')[3].text
            barCode = toInt(barCode)

        if 11 < len(soup.findAll('td')):
            commodityCode = soup.findAll('td')[11].text
            commodityCode = toInt(commodityCode)

        packSize = soup.find(string=re.compile('Pack Size'))
        packSize = toInt(packSize)

        rrp = soup.find(string=re.compile('RRP'))
        rrp = toFloat(rrp)

        if soup.find('span', {
                'class': 'col-xs-12 col-md-3 col-lg-3'}) != None:
            unitPrice = soup.find('span', {
                'class': 'col-xs-12 col-md-3 col-lg-3'}).findAll('span', {'class': 'highlight'})[0]
            unitPrice = toFloat(unitPrice)
        else:
            unitPrice = ''

        if soup.find('span', {'class': 'col-xs-12 col-md-3 col-lg-3'}) != None:
            packPrice = soup.find(
                'span', {'class': 'col-xs-12 col-md-3 col-lg-3'}).findAll('span', {'class': 'highlight'})[1]
            packPrice = toFloat(packPrice)
        else:
            packPrice = ''

        if soup.find('span', {'class': 'text-success highlight'}) != None:
            inStock = True
        else:
            inStock = False

        singleItemInfo['productURL'] = url
        singleItemInfo['imageURL'] = imageURL
        singleItemInfo['itemName'] = itemName
        singleItemInfo['productCode'] = productCode
        singleItemInfo['barCode'] = barCode
        singleItemInfo['commodityCode'] = commodityCode
        singleItemInfo['packSize'] = packSize
        singleItemInfo['rrp'] = rrp
        singleItemInfo['unitPrice'] = unitPrice
        singleItemInfo['packPrice'] = packSize
        singleItemInfo['inStock'] = inStock

        if singleItemInfo not in tags:
            logging.info(
                f'{currentTime()} {runIterator + 1} of {len(allJsonUrls)} {"{:.2f}".format(round((runIterator + 1) / len(allJsonUrls) * 100, 2))}% {singleItemInfo["productURL"]}')
            tags.append(singleItemInfo)
            singleItemInfo = {}

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileName = f'info-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/product-data/json/{fileName}', 'w') as f:
        json.dump(tags, f)

    return fileName


def jsonToCsv(fileName):
    logging.info(
        f'{currentTime()} WRITING PRODUCT INFO TO CSV')

    with open(f'output/product-data/json/{fileName}', 'r') as jsonFile:
        jsonData = json.load(jsonFile)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    with open(f'output/product-data/csv/info-nda-toys-{fileNameTimeStamp}.csv', 'w', newline='') as csvFile:

        fieldnames = ['productURL', 'imageURL', 'itemName', 'productCode',
                      'barCode', 'commodityCode', 'packSize', 'rrp', 'unitPrice', 'packPrice', 'inStock']

        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for row in jsonData:
            writer.writerow(row)

    logging.info(
        f'{currentTime()} Succesfullt written {len(jsonData)} products to CSV')


jsonToCsv(getProductInfo(writeProductLinksToJson(crawler(url))))
