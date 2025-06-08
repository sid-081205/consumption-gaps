import scrapy
import json
import logging

# Add selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logger = logging.getLogger(__name__)

class MorrisonsProductSpider(scrapy.Spider):

    name = 'morrisons_spider'
    allowed_domains = ['groceries.morrisons.com']
    
    start_urls = [
        'https://groceries.morrisons.com/search?q=bread']
    
    def start_requests(self):
        driver = webdriver.Chrome()

        for url in self.start_urls:
            logger.info(f"opening {url} with selenium for scrolling")
            driver.get(url)
            time.sleep(2)

            try:
                reject_btn = driver.find_element(By.ID, "onetrust-reject-all-handler")
                reject_btn.click()
                logger.info("clicked reject cookies button.")
                print("clicked reject cookies button.")
                time.sleep(1)
            except Exception:
                logger.info("reject cookies button not found or already handled.")

            last_height = driver.execute_script("return document.body.scrollHeight")
            max_attempts = 20
            attempts = 0
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "sc-filq44-0"))
                    )
                except Exception:
                    pass
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height or attempts >= max_attempts:
                    logger.info("selenium finished scrolling: reached end of page or max attempts.")
                    print("selenium finished scrolling: reached end of page or max attempts.")
                    break
                last_height = new_height
                attempts += 1
            driver.execute_script("window.scrollTo(0, 100);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            html = driver.page_source
            response = scrapy.http.HtmlResponse(url=url, body=html, encoding='utf-8')
            yield from self.parse(response)
        driver.quit()

    def parse(self, response):
        logger.info(f"processing search page: {response.url}")
        all_elements = response.xpath('//div[@class="sc-filq44-0.iAbOJh"]')
        logger.info(f"found {len(all_elements)} product containers")
        current_category = "No Category"
        products_found = 0
        for element in all_elements:
            header_text = element.xpath('.//div[@class="outer-header-container"]//span[@data-test="breadcrumb-text"]/text()').get()
            if header_text:
                current_category = header_text.strip()
                logger.info(f"found new category: {current_category}")
                continue
            product_data = self.extract_product_data(element, current_category, response)
            if product_data:
                products_found += 1
                logger.debug(f"extracted product {products_found}: {product_data['title']}")
                yield product_data
        logger.info(f"total products extracted: {products_found}")

    def extract_product_data(self, element, category, response):
        # title
        title = element.xpath('.//h3[@data-test="fop-title"]/text()').get()
        # link  
        link = element.xpath('.//a[@data-test="fop-product-link"]/@href').get()
        # price 
        price = element.xpath('.//span[@data-test="fop-price"]/text()').get()
        if title and price:
            if link:
                base_url = 'https://groceries.morrisons.com'
                absolute_link = base_url + link if link.startswith('/') else base_url + '/' + link
            else:
                absolute_link = None
            return {
                'category': category,
                'title': title.strip(),
                'price': price.strip(),
                'link': absolute_link,
            }
        else:
            logger.warning(f"Skipping incomplete product data: title={title}, price={price}")
            return None


