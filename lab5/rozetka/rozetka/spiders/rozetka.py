import scrapy
from bs4 import BeautifulSoup
# from rozetka.SeleniumRequest import SeleniumRequest
# from selenium.webdriver.support import expected_conditions
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from scrapy.http import JsonRequest
from scrapy.utils.serialize import ScrapyJSONEncoder

from rozetka.items import RozetkaItem

class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    allowed_domains = ['hard.rozetka.com.ua']
    BASE_URL = 'hard.rozetka.com.ua'
    start_urls = ['https://hard.rozetka.com.ua/ua/monitors/c80089/']
    encode = ScrapyJSONEncoder().encode
    temporary_item = {}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        last_page = int(soup.find(class_="pagination").find(class_="pagination__list")
                        .find_all(class_="pagination__item")[-1].find('a').getText())
        for i in range(1, last_page + 1):
            yield scrapy.Request(
                url=f'{self.start_urls[0]}page={i}',
                callback=self.parse_monitors
            )


    def parse_monitors(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        monitors_list = soup.find(class_="catalog-grid").find_all(class_="catalog-grid__cell")

        for monitor in monitors_list:
            model_tag = monitor.find(class_="goods-tile__heading")
            model = model_tag.getText().replace('"', '').strip()
            price = int(monitor.find(class_="goods-tile__price-value").getText().replace('\xa0', '').strip())
            link = model_tag.get("href")

            self.temporary_item = RozetkaItem(model=model, price=price, link=link)
            yield self.temporary_item

    def create_item(self):
        return JsonRequest(
            url='https://localhost:44349/monitors',
            method='POST',
            body=self.encode(self.temporary_item),
            dont_filter=True
        )

    def update_item(self, responce):
        print('update//////////////////////////////////////////////////')

        return JsonRequest(
            url='https://localhost:44349/monitors',
            method='PUT',
            body=self.encode(self.temporary_item),
            dont_filter=True
        )