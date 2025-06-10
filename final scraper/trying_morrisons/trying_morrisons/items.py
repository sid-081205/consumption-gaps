# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy # type: ignore


class TryingMorrisonsItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    energy_per_100g = scrapy.Field()
    fat_per_100g = scrapy.Field()
    saturated_fat_per_100g = scrapy.Field()
    protein_per_100g = scrapy.Field()
