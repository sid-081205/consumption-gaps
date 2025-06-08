# web-scraping-project

## description

a project to scrape product data from various grocery store websites in the uk for price and nutrition comparison. thought a visualization with the best health benefits in each product category could come useful. imagine a graph for each search query which shows which products have the best protein/carb/fat ratios

## scraping_journey

all scraping attempts are coded and tested in this repo.

successfully scraped product data using selenium and sainsbury's hidden api.

ran into trouble with dynamic dropdowns inside sainsbury's product page, so tried scrapy, but antibot protection blocked me. 

got comfortable with using the scrapy shell and making xpath/css selectors

tesco banned my ip for 2 days (not messing with them again). asda also has strong antibot protection - interestingly the html says "REQUEST INTERCEPTED" which was fun.

currently, the only option is to try iceland, but i haven't figured out how to handle dynamic javascript dropdowns in html. 

tried morrisons — nutritional data is available without dynamic content. ran into some 403 errors with scrapy, but tweaking the settings to be more realistic helped avoid detection.

morrisons is great: every result has a category, so it's easy to split and compare products. would be cool to let users filter by category—might add that.

## hybrid approach: selenium + scrapy

for morrisons, i use selenium to grab product info (title, price, category, link) from search results, then scrapy to visit each link and extract nutrition data. this two-step method handles dynamic pages and antibot blocks.





