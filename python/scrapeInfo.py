import csv
import datetime
import json
import logging
import re
import requests
import time
from bs4 import BeautifulSoup
from os import error

startTime = time.time()

fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d')

with open(f'output/logs/log-{fileNameTimeStamp}.log', 'w') as logfile:
    logging.basicConfig(
        filename=f'output/logs/log-{fileNameTimeStamp}.log', level=logging.INFO)

logging.info('========== SEARCHING FOR PRODUCTS ==========')

url = 'https://www.nda-toys.com/'

all_product_links = set()
all_page_links = set()
all_links = set()


def crawler(url):
    all_links.add(url)
    logging.info(f'{time.strftime("%M:%S",  time.gmtime(time.time() - startTime))} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Checking... {url}')

    try:
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        pageTags = soup.find_all("a")

        for pageTag in pageTags:
            tag = str(pageTag.get('href'))
            if tag not in all_product_links and 'https://www.nda-toys.com/product/' in tag:
                all_product_links.add(tag)
                all_links.add(tag)
                logging.info(
                    f'{time.strftime("%M:%S",  time.gmtime(time.time() - startTime))} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Product link... {tag}')

            elif 'page=' in tag and tag not in all_page_links:
                all_page_links.add(tag)
                all_links.add(tag)
                logging.info(
                    f'{time.strftime("%M:%S",  time.gmtime(time.time() - startTime))} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | New page... {tag}')

                crawler(tag)

            elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
                all_links.add(tag)
                crawler(tag)

    except:
        logging.info(f'{error} in url {url}, tag {tag}')

    return all_product_links


def writeProductLinksToJson(all_product_links):

    logging.info('========== WRITING PRODUCT LINKS TO JSON ==========')

    all_product_links = list(all_product_links)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileNameTwo = f'links-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/link-data/{fileNameTwo}', 'w') as f:
        json.dump(all_product_links, f)

    logging.info(
        f'Succesfullt written {len(all_product_links)} product links to JSON')
    logging.info(fileNameTwo)

    return fileNameTwo


def getProductInfo(fileName):
    startTime = time.time()

    logging.info('========== GETTING PRODUCT INFO ==========')
    logging.info(fileName)
    logging.info(f'output/link-data/{fileName}')

    fPath = f'output/link-data/{fileName}'
    logging.info(f'{fPath}')

    with open(fPath, 'r') as jsonFile:
        logging.info(jsonFile)
        allJsonUrls = json.load(jsonFile)

    singleItemInfo = {}
    tags = []

    for runIterator, url in enumerate(allJsonUrls):
        # try:
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
        singleItemInfo['barCode'] = int(barCode.text)
        singleItemInfo['commodityCode'] = re.sub(
            '\D', '', commodityCode.text)
        singleItemInfo['packSize'] = re.sub(
            '\D', '', packSize.text)
        singleItemInfo['rrp'] = re.search(
            '\d*[.]\d*', rrp.text).group()
        singleItemInfo['unitPrice'] = re.search(
            '\d*[.]\d*', unitPrice.text).group()
        singleItemInfo['packPrice'] = re.search(
            '\d*[.]\d*', packPrice.text).group()

        if singleItemInfo not in tags:
            logging.info(
                f'{runIterator + 1} of {len(allJsonUrls)} {round((runIterator + 1) / len(allJsonUrls) * 100, 2)}% {time.strftime("%M:%S",  time.gmtime(time.time() - startTime))} {singleItemInfo["barCode"]} {singleItemInfo["productURL"]}')
            tags.append(singleItemInfo)
            singleItemInfo = {}
        # except:
        #     logging.info(f'Error {error}')
        #     logging.info(f'Error {error.strerror}')
        #     logging.info(f'Error {error.winerror}')

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileName = f'info-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/product-data/json/{fileName}', 'w') as f:
        json.dump(tags, f)

    return fileName


def jsonToCsv(fileName):
    logging.info('========== WRITING PRODUCT INFO TO CSV ==========')

    with open(f'output/product-data/json/{fileName}', 'r') as jsonFile:
        jsonData = json.load(jsonFile)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    with open(f'output/product-data/csv/info-nda-toys-{fileNameTimeStamp}.csv', 'w', newline='') as csvFile:

        fieldnames = ['productURL', 'productImageURL', 'itemName', 'productCode',
                      'barCode', 'commodityCode', 'packSize', 'rrp', 'unitPrice', 'packPrice']

        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for row in jsonData:
            writer.writerow(row)

    logging.info(f'Succesfullt written {len(jsonData)} products to CSV')


jsonToCsv(getProductInfo(writeProductLinksToJson(crawler(url))))
