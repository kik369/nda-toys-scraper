import csv
import datetime
import json
import logging
import re
import requests
from bs4 import BeautifulSoup


fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d')

with open(f'output/logs/log-{fileNameTimeStamp}.log', 'w') as logfile:
    logging.basicConfig(
        filename=f'output/logs/log-{fileNameTimeStamp}.log', level=logging.INFO)

logging.info(
    f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} SEARCHING FOR PRODUCTS')

url = 'https://www.nda-toys.com/'

all_product_links = set()
all_page_links = set()
all_links = set()


def crawler(url):
    all_links.add(url)
    logging.info(f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Checking... {url}')

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
                f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | Product link... {tag}')

        elif 'page=' in tag and tag not in all_page_links:
            all_page_links.add(tag)
            all_links.add(tag)
            logging.info(
                f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} | Products: {len(all_product_links)} | Pages: {len(all_page_links)} | URLs: {len(all_links)} | New page... {tag}')

            crawler(tag)

        elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
            all_links.add(tag)
            crawler(tag)

    return all_product_links


def writeProductLinksToJson(all_product_links):

    logging.info(
        f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} WRITING PRODUCT LINKS TO JSON')

    all_product_links = list(all_product_links)

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileName = f'links-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/link-data/{fileName}', 'w') as f:
        json.dump(all_product_links, f)

    logging.info(
        f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} Succesfullt written {len(all_product_links)} product links to JSON')

    return fileName


def getProductInfo(fileName):

    logging.info(
        f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} GETTING PRODUCT INFO')

    fPath = f'output/link-data/{fileName}'

    with open(fPath, 'r') as jsonFile:
        allJsonUrls = json.load(jsonFile)

    singleItemInfo = {}
    tags = []

    for runIterator, url in enumerate(allJsonUrls):
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

        if soup.find("span", {
                "class": "col-xs-12 col-md-3 col-lg-3"}) != None:
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
                f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} {runIterator + 1} of {len(allJsonUrls)} {"{:.2f}".format(round((runIterator + 1) / len(allJsonUrls) * 100, 2))} % {singleItemInfo["productURL"]}')
            tags.append(singleItemInfo)
            singleItemInfo = {}

    fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    fileName = f'info-nda-toys-{fileNameTimeStamp}.json'
    with open(f'output/product-data/json/{fileName}', 'w') as f:
        json.dump(tags, f)

    return fileName


def jsonToCsv(fileName):
    logging.info(
        f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} WRITING PRODUCT INFO TO CSV')

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

    logging.info(
        f'{datetime.datetime.today().strftime("%Y/%m/%d @ %H:%M:%S")} Succesfullt written {len(jsonData)} products to CSV')


jsonToCsv(getProductInfo(writeProductLinksToJson(crawler(url))))
