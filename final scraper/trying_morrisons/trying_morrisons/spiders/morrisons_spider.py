import json
import scrapy
import logging
import csv
from trying_morrisons.items import TryingMorrisonsItem

logger = logging.getLogger(__name__)

class MorrisonsProductSpider(scrapy.Spider):
    name = 'morrisons_spider'
    allowed_domains = ['groceries.morrisons.com']
    
    def start_requests(self):
        with open('/Users/siddharthgianchandani/Desktop/vscode projects/consumption-gaps/final scraper/products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield scrapy.Request(
                    url=row['link'],
                    callback=self.parse,
                    meta={
                        'category': row['category'],
                        'title': row['title'],
                        'price': row['price'],
                        'link': row['link']
                    }
                )

    def parse(self, response):
        item = TryingMorrisonsItem()
        item['category'] = response.meta['category']
        item['title'] = response.meta['title']
        item['price'] = response.meta['price']
        item['link'] = response.meta['link']
        item['energy_per_100g'] = response.css('table.nutrition tr:contains("Energy") td:nth-child(2)::text').get()
        item['fat_per_100g'] = response.css('table.nutrition tr:contains("Fat") td:nth-child(2)::text').get()
        item['saturated_fat_per_100g'] = response.css('table.nutrition tr:contains("saturates") td:nth-child(2)::text').get()
        item['protein_per_100g'] = response.css('table.nutrition tr:contains("Protein") td:nth-child(2)::text').get()
        yield item
