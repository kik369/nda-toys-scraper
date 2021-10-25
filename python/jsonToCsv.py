import csv
import json
import datetime
import os


def jsonToCsv():

    path = 'output/product-data/json/'

    for fileName in os.listdir(path):

        if fileName[:24] == datetime.datetime.today().strftime('info-nda-toys-%Y-%m-%d'):
            print(fileName[:24])
            with open(f'output/product-data/json/{fileName}', 'r') as jsonFile:
                jsonData = json.load(jsonFile)

            fileNameTimeStamp = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

            with open(f'output/product-data/csv/info-nda-toys-{fileNameTimeStamp}.csv', 'w', newline='') as csvFile:

                fieldnames = ['productURL', 'productImageURL', 'itemName', 'productCode',
                              'barCode', 'commodityCode', 'packSize', 'rrp', 'unitPrice', 'packPrice']

                spamwriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
                spamwriter.writeheader()

                for row in jsonData:
                    spamwriter.writerow(row)
                    print(row)
