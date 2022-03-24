import csv
import datetime
import json
import logging
import re

import requests
from bs4 import BeautifulSoup

# global all_product_links
all_product_links = set()
# global all_page_links
all_page_links = set()
# global all_links
all_links = set()

def d_t_stamp():
    return datetime.datetime.today().strftime('%Y/%m/%d @ %H:%M:%S')

def f_n_t_stamp():
    return datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

def log_stats_and_url(string, url):
    logging.info(f'{d_t_stamp()} | '
    f'Products: {len(all_product_links)} | '
    f'Pages: {len(all_page_links)} | '
    f'URLs: {len(all_links)} | {string}... {url}')

def crawler(url):
    all_links.add(url)
    log_stats_and_url('Checking', url)

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    pageTags = soup.find_all('a')

    for pageTag in pageTags:
        tag = str(pageTag.get('href'))
        if tag not in all_product_links and 'https://www.nda-toys.com/product/' in tag:
            all_product_links.add(tag)
            all_links.add(tag)
            log_stats_and_url('Product link', tag)

        elif 'page=' in tag and tag not in all_page_links:
            all_page_links.add(tag)
            all_links.add(tag)
            log_stats_and_url('New page', tag)

            crawler(tag)

        elif tag not in all_links and 'https://www.nda-toys.com/' in tag and 'sort=' not in tag and '?f' not in tag and '.jpg' not in tag:
            all_links.add(tag)
            crawler(tag)

    return all_product_links


def write_product_links_to_json(all_product_links):
    logging.info(
        f'{d_t_stamp()} WRITING PRODUCT LINKS TO JSON')
    all_product_links = list(all_product_links)
    file_name_time_stamp = f_n_t_stamp()
    file_name = f'links-nda-toys-{file_name_time_stamp}.json'
    with open(f'output/link-data/{file_name}', 'w') as f:
        json.dump(all_product_links, f)

    logging.info(
        f'{d_t_stamp()} Succesfullt written {len(all_product_links)} product links to JSON')

    return file_name


def str_to_int(string):
    """replaces non digits (\D) with an empty string and returns an int"""
    if string != None:
        string = re.sub('\D', '', string)
        if string != '':
            string = int(string)
    return string


def str_to_float(string):
    if string != None:
        string = re.search('\d*[.]\d*', string.text).group()
        string = '{:.2f}'.format(float(string))
        string = float(string)
    return string


def get_product_info(file_name):

    logging.info(
        f'{d_t_stamp()} GETTING PRODUCT INFO')

    fPath = f'output/link-data/{file_name}'

    with open(fPath, 'r') as jsonFile:
        allJsonUrls = json.load(jsonFile)

    singleItemInfo = {}
    tags = []

    for runIterator, url in enumerate(allJsonUrls):
        response = requests.get(url)

        if response.status_code == 200:

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
                productCode = str_to_int(productCode)

            if 3 < len(soup.findAll('td')):
                barCode = soup.findAll('td')[3].text
                barCode = str_to_int(barCode)

            if 11 < len(soup.findAll('td')):
                commodityCode = soup.findAll('td')[11].text
                commodityCode = str_to_int(commodityCode)

            packSize = soup.find(string=re.compile('Pack Size'))
            packSize = str_to_int(packSize)

            rrp = soup.find(string=re.compile('RRP'))
            rrp = str_to_float(rrp)

            if soup.find('span', {
                    'class': 'col-xs-12 col-md-3 col-lg-3'}) != None:
                unitPrice = soup.find('span', {
                    'class': 'col-xs-12 col-md-3 col-lg-3'}).findAll('span', {'class': 'highlight'})[0]
                unitPrice = str_to_float(unitPrice)
            else:
                unitPrice = ''

            if soup.find('span', {'class': 'col-xs-12 col-md-3 col-lg-3'}) != None:
                packPrice = soup.find(
                    'span', {'class': 'col-xs-12 col-md-3 col-lg-3'}).findAll('span', {'class': 'highlight'})[1]
                packPrice = str_to_float(packPrice)
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
            singleItemInfo['packPrice'] = packPrice
            singleItemInfo['inStock'] = inStock

            if singleItemInfo not in tags:
                logging.info(
                    f'{d_t_stamp()} {runIterator + 1} of {len(allJsonUrls)} {"{:.2f}".format(round((runIterator + 1) / len(allJsonUrls) * 100, 2))}% {singleItemInfo["productURL"]}')
                tags.append(singleItemInfo)
                singleItemInfo = {}

    file_name_time_stamp = f_n_t_stamp()
    file_name = f'info-nda-toys-{file_name_time_stamp}.json'
    with open(f'output/product-data/json/{file_name}', 'w') as f:
        json.dump(tags, f)

    return file_name


def jsonToCsv(fileName):
    logging.info(
        f'{d_t_stamp()} WRITING PRODUCT INFO TO CSV')

    with open(f'output/product-data/json/{fileName}', 'r') as jsonFile:
        jsonData = json.load(jsonFile)

    file_name_time_stamp = f_n_t_stamp()

    with open(f'output/product-data/csv/info-nda-toys-{file_name_time_stamp}.csv', 'w', newline='') as csvFile:

        fieldnames = ['productURL', 'imageURL', 'itemName', 'productCode',
                      'barCode', 'commodityCode', 'packSize', 'rrp', 'unitPrice', 'packPrice', 'inStock']

        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        for row in jsonData:
            writer.writerow(row)

    logging.info(
        f'{d_t_stamp()} Succesfullt written {len(jsonData)} products to CSV')


# jsonToCsv(getProductInfo(writeProductLinksToJson(crawler(url))))

def set_up_logging():
    file_name_time_stamp = datetime.datetime.today().strftime('%Y-%m-%d')
    log_file = f'output/logs/log-{file_name_time_stamp}.log'
    open(log_file, 'w')
    logging.basicConfig(filename=log_file, level=logging.INFO)


def main():
    set_up_logging()

    url = 'https://www.nda-toys.com/'

    logging.info(f'{d_t_stamp()} SEARCHING FOR PRODUCTS')

    all_product_links = crawler(url)
    file_name = write_product_links_to_json(all_product_links)
    file_name = get_product_info(file_name)
    jsonToCsv(file_name)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
