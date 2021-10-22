var fs = require('fs');
var obj = JSON.parse(fs.readFileSync('./python/details.json', 'utf8'));

const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
  path: 'output.csv',
  header: [
    { id: 'productURL', title: 'productURL' },
    { id: 'productImageURL', title: 'productImageURL' },
    { id: 'itemName', title: 'itemName' },
    { id: 'productCode', title: 'productCode' },
    { id: 'barCode', title: 'barCode' },
    { id: 'commodityCode', title: 'commodityCode' },
    { id: 'packSize', title: 'packSize' },
    { id: 'rrp', title: 'rrp' },
    { id: 'unitPrice', title: 'unitPrice' },
    { id: 'packPrice', title: 'packPrice' },
  ],
});

csvWriter.writeRecords(obj).then(() => console.log('The CSV file was written successfully'));
